"""An app that presents a window for picking countries. Country data is fetched from a server."""

from PyQt6 import QtWidgets
import form_window
from data_fetcher import CountryFetcher
import typing
import threading
import sys

if __name__ == "__main__":
        
    application: QtWidgets.QApplication = QtWidgets.QApplication([])

    window: form_window.AppWindow = form_window.AppWindow()

    countries_url = "https://www.apicountries.com/countries"
    data_fetcher: CountryFetcher = CountryFetcher(countries_url, window.country_picker.addItems)

    window.show()

    data_fetcher.start_data_fetch_thread()

    application.exec()