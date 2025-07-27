'''To test the json-parsing. Run pytest to make sure it passes. '''

import data_fetcher
import requests_mock
from data_fetcher import CountryFetcher
import requests

def test_json():
    received_text = '[{"name":"Afghanistan","topLevelDomain":[".af"],"alpha2Code":"AF","alpha3Code":"AFG","callingCodes":["93"],"capital":"Kabul","altSpellings":["AF","Afġānistān"],"subregion":"Southern Asia","region":"Asia","population":40218234,"latlng":[33,65],"demonym":"Afghan","area":652230,"timezones":["UTC+04:30"],"borders":["IRN","PAK","TKM","UZB","TJK","CHN"],"nativeName":"افغانستان","numericCode":"004","flags":{"svg":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_the_Taliban.svg","png":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_the_Taliban.svg/320px-Flag_of_the_Taliban.svg.png"},"currencies":[{"code":"AFN","name":"Afghan afghani","symbol":"؋"}],"languages":[{"iso639_1":"ps","iso639_2":"pus","name":"Pashto","nativeName":"پښتو"},{"iso639_1":"uz","iso639_2":"uzb","name":"Uzbek","nativeName":"Oʻzbek"},{"iso639_1":"tk","iso639_2":"tuk","name":"Turkmen","nativeName":"Türkmen"}],"translations":{"br":"Afghanistan","pt":"Afeganistão","nl":"Afghanistan","hr":"Afganistan","fa":"افغانستان","de":"Afghanistan","es":"Afganistán","fr":"Afghanistan","ja":"アフガニスタン","it":"Afghanistan","hu":"Afganisztán"},"flag":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_the_Taliban.svg","regionalBlocs":[{"acronym":"SAARC","name":"South Asian Association for Regional Cooperation"}],"cioc":"AFG","independent":true}]'

    with requests_mock.Mocker() as mocker:
        mocker.get("https://www.apicountries.com/countries", text=received_text) # fake the HTTP connection.

        url = "https://www.apicountries.com/countries"
        def fake_slot(list_of_strings: list[str]) -> None: return # fake the slot.

        country_list = CountryFetcher(url, fake_slot).try_fetch_countries() #so it's the JSON-parsing that is being tested.

        assert country_list is not None, "A list of countries was not attained."
        assert "Afghanistan" in country_list, "the country 'Afghanistan' is missing from the list."
    

test_json()