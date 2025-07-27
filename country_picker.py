"""An app that presents a window containing a blank label and ComboBox."""

from PyQt6 import QtWidgets
import form_window
import data_fetcher
import typing

if __name__ == "__main__":

    application: QtWidgets.QApplication = QtWidgets.QApplication([])

    window: form_window.AppWindow = form_window.AppWindow()
    window.show()

    countries_url = "https://www.apicountries.com/countries"
    country_list: list[str] | None = data_fetcher.try_fetch_countries(countries_url)

    if country_list is not None:
        window.update_country_list(country_list)
    
    application.exec()