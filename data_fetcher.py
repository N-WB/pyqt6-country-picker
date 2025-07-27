import requests
import typing
from typing import Any, Callable
import country_validation
from PyQt6.QtCore import QThread


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
        '''Start a thread that will attempt to obtain countries data until it succeeds.'''
        def pushCountryData():
            if self._country_names is not None:
                self._slot(self._country_names)

        self.finished.connect(pushCountryData)
        self.start()


    def run(self) -> None:
        ms_between_attempt_groups = 1000

        while self._country_names is None:
            
            self._country_names = self.try_fetch_countries()
            if self._country_names is not None: break

            self.msleep(ms_between_attempt_groups)

        self.quit()
    

    def try_fetch_countries(self) -> list[str] | None:
        ''' Attempts to GET countries. Returns the list of countries, or None if any error is encountered.'''
        
        response = requests.get(self._url)
        try:
            response = requests.get(self._url)
        except requests.RequestException as error:
            print(error)
            return None
            
        if response.status_code is not requests.codes.ok:
            print("Error: received network error", response.status_code)
            return None


        jsonAsPythonObject = None
        try:
            jsonAsPythonObject = response.json()
        except requests.exceptions.JSONDecodeError as error:
            print(error)
            return None
        
        
        is_valid = country_validation.do_full_country_list_validation(jsonAsPythonObject)            
        if is_valid:
            def extract_name(country): return country["name"]
            country_names = [extract_name(c) for c in jsonAsPythonObject]
            country_names.sort()
            return country_names
        else:
            print("Error: the received json does not conform to the expected countries format.")
            return None


        
        