"""An app that presents a window for picking countries. Country data is fetched from a server."""

from PyQt6 import QtWidgets
import form_window
from data_fetcher import CountryFetcher
import typing
import sys


def consumeCommandLineArgs() -> str | None:
    '''If --select is provided as the second command-line argument, then the third item is used as the default combobox value.'''
    defaultCountry = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--select":
        defaultCountry = sys.argv[2]
    return defaultCountry


if __name__ == "__main__":

    defaultCountry = consumeCommandLineArgs()
        
    application: QtWidgets.QApplication = QtWidgets.QApplication([])

    window: form_window.AppWindow = form_window.AppWindow()
    def slot_for_fetched_data(country_names: list[str]) -> None:
        window.country_picker.addItems(country_names)
        if defaultCountry is not None:
            window.country_picker.setCurrentText(defaultCountry)

    countries_url = "https://www.apicountries.com/countries"
    data_fetcher: CountryFetcher = CountryFetcher(countries_url, slot_for_fetched_data)

    window.show()

    data_fetcher.start_data_fetch_thread()

    application.exec()