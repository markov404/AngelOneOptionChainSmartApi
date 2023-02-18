
import time
import requests

from smartapi import SmartConnect


class App:
    def __init__(self, usr, api_key) -> None:
        self.__user = usr
        self.__api_key = api_key

        self.__smart = SmartConnect(self.__api_key)
        self.__url_for_instruments = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        self.__instrument_list = []

    def start_session(self) -> dict:
        def request_for_session() -> dict:
            attempts = 5
            while attempts > 0:
                attempts = attempts - 1
                data = self.__smart.generateSession(
                    self.__user.usr_id,
                    self.__user.password,
                    self.__user.totp
                )

                if data['status']:
                    __JWT_TOKEN = data['data']['jwtToken']
                    __FEED_TOKEN = self.__smart.getfeedToken()
                    return {
                        "status": "success",
                        "data": data,
                        "additionalData": {
                            "JWT": __JWT_TOKEN,
                            "FEED": __FEED_TOKEN}}

                time.sleep(2)

            return {"status": "error", "data": data}

        return request_for_session()

    def download_and_update_instrument_list(self) -> None:
        self.__instrument_list.clear()
        self.__instrument_list = requests.get(
            self.__url_for_instruments).json()

    def get_options_map(self, exch_type="NFO", opt_type="OPTIDX") -> list:
        instrument_list = self.__instrument_list
        options_map = []

        for instrument in instrument_list:
            st1 = (instrument['exch_seg'] == exch_type)
            st2 = (instrument['instrumenttype'] == opt_type)
            if st1 and st2:
                options_map.append(instrument)

        return options_map
