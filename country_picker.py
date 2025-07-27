"""An app that presents a window for picking countries. Country data is fetched from a server."""

import typing
from typing import Any, Callable

import compose
import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread

import requests





def format_country_name(country_name: str) -> str:
    return "Selected: " + country_name

class AppWindow(QtWidgets.QMainWindow):
    """An application window containing a label and combobox for picking countries"""
    
    central_widget: QtWidgets.QWidget
    selected_country_label: QtWidgets.QLabel
    country_picker: QtWidgets.QComboBox
    countries_data: list[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.setGeometry(20, 20, 600, 400)
        self.setWindowTitle("Country Picker")
        
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        new_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(new_layout)


        self.selected_country_label = QtWidgets.QLabel()
        new_layout.addWidget(self.selected_country_label)
        
        self.country_picker = QtWidgets.QComboBox()
        new_layout.addWidget(self.country_picker)

        slot = compose.compose(self.selected_country_label.setText, format_country_name)
        self.country_picker.currentTextChanged.connect(slot)
        
        self.show()




class CountryFetcher(QThread):
    '''
    Fetches country name data from the url and notifies the slot once complete.

    If the resulting data is bad then this object will intermittently attempt the process again.
    '''

    _country_names: list[str] | None
    _url: str
    #_slot: PYQT_SLOT # N.B. had issues importing the type PYQT_SLOT - but this would be ideal to fix


    def __init__(self, countries_url: str, slot: Callable[[list[str]], None]) -> None:
        QThread.__init__(self)
        self._url = countries_url
        self._slot = slot
        self._country_names = None


    def start_data_fetch_thread(self) -> None:
        def pushCountryData():
            if self._country_names is not None:
                self._slot(self._country_names)

        self.finished.connect(pushCountryData)
        self.start()


    def run(self) -> None:
        ms_between_attempt_groups = 1000 # delay of 1000 is arbitrary

        while self._country_names is None:
            
            self._country_names = self.try_fetch_countries()
            if self._country_names is not None: break

            self.msleep(ms_between_attempt_groups)

        self.quit()
    

    def try_fetch_countries(self) -> list[str] | None:
        ''' Attempts to GET countries. Returns the list of countries, or None if any error is encountered.'''
        try:
            response = requests.get(self._url)
        except requests.RequestException as error:
            print(error)
            return None
            
        if response.status_code is not requests.codes.ok:
            print("A")
            print("Error: received network error", response.status_code)
            print("B")
            return None


        jsonAsPythonObject = None
        try:
            jsonAsPythonObject = response.json()
        except requests.exceptions.JSONDecodeError as error:
            print(error)
            return None
        
        
        is_valid = do_full_country_list_validation(jsonAsPythonObject)            
        if is_valid:
            def extract_name(country): return country["name"]
            country_names = [extract_name(c) for c in jsonAsPythonObject]
            country_names.sort()
            return country_names
        else:
            print("Error: the received json does not conform to the expected countries format.")
            return None




def validate_list_of_entries(   
          maybe_list: Any
        , per_item_validator: Callable[[Any], bool]
    ) -> bool:
    '''Checks that all items in a list of entries are valid.'''

    if not isinstance(maybe_list, list):
        return False
    
    for item in maybe_list:
        is_item_valid: bool = per_item_validator(item)
        if not is_item_valid:
            return False
        
    return True


def check_country_has_name(country_object: Any) -> bool:
    return "name" in country_object and isinstance(country_object["name"], str)


def do_full_country_list_validation(countries_list: Any) -> bool:
    '''Perform all the necessary validations on a list of countries.'''

    # ponder - consider doing full validation of all the fields of the country versus just the field "name" that we need

    # N.B. the types implied by the countries API documentation are ambiguous
    # In the API, only 165 countries have a "borders" attribute, despite the fact that "https://www.apicountries.com/docs/api/countries"
    # implies that the borders attribute is present on all types.

    return validate_list_of_entries(countries_list, check_country_has_name)





def consumeCommandLineArgs() -> str | None:
    '''If --select is provided as the second command-line argument, then the third item is used as the default combobox value.'''
    defaultCountry = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--select":
        defaultCountry = sys.argv[2]
    return defaultCountry


if __name__ == "__main__":

    defaultCountry = consumeCommandLineArgs()
        
    application: QtWidgets.QApplication = QtWidgets.QApplication([])

    window: AppWindow = AppWindow()
    def slot_for_fetched_data(country_names: list[str]) -> None:
        window.country_picker.addItems(country_names)
        if defaultCountry is not None:
            window.country_picker.setCurrentText(defaultCountry)

    countries_url = "https://www.apicountries.com/countries"
    data_fetcher: CountryFetcher = CountryFetcher(countries_url, slot_for_fetched_data)

    window.show()

    data_fetcher.start_data_fetch_thread()

    application.exec()