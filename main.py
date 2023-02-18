

import time
import os

from settings import InitSettings

from components.utlis import (
    check_on_error,
    sort_by_name_of_option_and_split_result_on_chunks as smart_sort,
    make_token_list_for_web_socket as token_list,
    make_set_of_option_names as make_option_names
)

from components.smart_api_web_sock_v2 import SmartWebSocketV2
from components.user import User
from components.app import App
from components.output_processor import OutputProcessor

OUR_PATH = os.getcwd()


def get_data_using_socket(
        usr: User,
        api_key: str,
        options_map: list,
        case_to_work: int,
        name: str,
        OutputManager: OutputProcessor) -> None:

    global cases_counter
    cases_counter = 0

    def on_data(wsapp, message):
        check_on_error(message)

        token = message['token']
        for option in options_map:
            if option['token'] == token:
                option.update(message)
        global cases_counter

        cases_counter += 1

        if cases_counter == case_to_work:
            sws.unsubscribe(CORRELATION_ID, MODE, TOKENS_AND_PROPERTIES)
            sws.close_connection()
            OutputManager.collect_data(options_map, name)

    def on_open(wsapp):
        print("on open")
        sws.subscribe(CORRELATION_ID, MODE, TOKENS_AND_PROPERTIES)

    def on_error(wsapp, error):
        print(f"ERROR - {error}")
        sws.resubscribe()

    def on_close(wsapp):
        print("Close")

    CORRELATION_ID = "123_qwerty"  # dummy actually
    MODE = 3  # Means it is Snap Quote mode
    TOKENS_AND_PROPERTIES = [
        {"exchangeType": 2,  # Means we are getting data on NFO
         "tokens": token_list(options_map)}]

    sws = SmartWebSocketV2(usr.jwt, api_key, usr.usr_id, usr.feed)
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    try:
        sws.connect()
    except BaseException:
        sws.unsubscribe(CORRELATION_ID, MODE, TOKENS_AND_PROPERTIES)
        sws.close_connection()


def start_app(usr: User, api_key: str, options_map: list):

    option_names = make_option_names(options_map)
    dictionary_of_options = smart_sort(options_map, option_names)

    OutputManager = OutputProcessor(f"{OUR_PATH}\\")

    while True:
        for name_and_options in dictionary_of_options.items():
            name = name_and_options[0]
            list_of_options_lists = name_and_options[1]
            for option_list in list_of_options_lists:
                get_data_using_socket(
                    usr,
                    api_key,
                    option_list,
                    len(option_list),
                    name,
                    OutputManager)

        OutputManager.print()
        OutputManager.clear_buffer()
        print("Sleeping...")
        time.sleep(180)


def main():
    stng = InitSettings(f"{OUR_PATH}\\settings.txt")

    usr = User(stng.ID, stng.PASSWORD, stng.OTP_CODE)
    app = App(
        usr=usr,
        api_key=stng.API_KEY
    )

    JWT = ""
    FEED = ""
    smart_api_response = app.start_session()
    if smart_api_response["status"] == "error":
        raise Exception("Can`t start the session with SmartApi")
    else:
        JWT = smart_api_response["additionalData"]["JWT"]
        usr.jwt = JWT
        FEED = smart_api_response["additionalData"]["FEED"]
        usr.feed = FEED

    app.download_and_update_instrument_list()
    options_map = app.get_options_map()

    start_app(
        usr=usr,
        api_key=stng.API_KEY,
        options_map=options_map
    )


try:
    main()
except Exception as E:
    print(E)
    waiting = input('Type in anything to close programm...')
