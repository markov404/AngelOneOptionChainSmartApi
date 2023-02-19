
from datetime import datetime
from schema import Schema, Optional, And

"""
OPTION DATA EXAMPLE:

{
    'token': '47338',
    'symbol': 'NIFTY09MAR2318050CE',
    'name': 'NIFTY',
    'expiry': '09MAR2023',
    'strike': '1805000.000000',
    'lotsize': '50',
    'instrumenttype': 'OPTIDX',
    'exch_seg': 'NFO',
    'tick_size': '5.000000',
    'subscription_mode': 3,
    'exchange_type': 2,
    'sequence_number': 46136693,
    'exchange_timestamp': 1676455199000,
    'last_traded_price': 32525,
    'subscription_mode_val': 'SNAP_QUOTE',
    'last_traded_quantity': 100,
    'average_traded_price': 32525,
    'volume_trade_for_the_day': 100,
    'total_buy_quantity': 2300.0,
    'total_sell_quantity': 2250.0,
    'open_price_of_the_day': 32525,
    'high_price_of_the_day': 32525,
    'low_price_of_the_day': 32525,
    'closed_price': 26205,
    'last_traded_timestamp': 1676454403,
    'open_interest': 100,
    'open_interest_change_percentage': 0,
    'upper_circuit_limit': 75910,
    'lower_circuit_limit': 5,
    '52_week_high_price': 211815,
    '52_week_low_price': 0,
    'best_5_buy_data': [{
        'flag': 0,
        'quantity': 900,
        'price': 22420,
        'no of orders': 1
    }, {
        'flag': 0,
        'quantity': 50,
        'price': 22430,
        'no of orders': 1
    }, {
        'flag': 0,
        'quantity': 850,
        'price': 23205,
        'no of orders': 1
    }, {
        'flag': 0,
        'quantity': 200,
        'price': 32000,
        'no of orders': 1
    }, {
        'flag': 0,
        'quantity': 200,
        'price': 70000,
        'no of orders': 1
    }],
    'best_5_sell_data': [{
        'flag': 1,
        'quantity': 50,
        'price': 20060,
        'no of orders': 1
    }, {
        'flag': 1,
        'quantity': 200,
        'price': 20055,
        'no of orders': 1
    }, {
        'flag': 1,
        'quantity': 900,
        'price': 19755,
        'no of orders': 1
    }, {
        'flag': 1,
        'quantity': 600,
        'price': 10200,
        'no of orders': 1
    }, {
        'flag': 1,
        'quantity': 500,
        'price': 20,
        'no of orders': 1
    }]
}

"""


class OutputProcessor:
    options_store_key_name_SCHEMA = Schema(
        {
            str: {
                str: {
                    And(str, lambda s: (s == 'CE' or s == 'PE')): dict
                }
            }
        }
    )

    options_map_SCHEMA = Schema([{
        'token': str,
        'symbol': str,
        'name': str,
        'expiry': str,
        'strike': str,
        'lotsize': str,
        'instrumenttype': str,
        'exch_seg': str,
        'tick_size': str,
        'subscription_mode': int,
        'exchange_type': int,
        'sequence_number': int,
        'exchange_timestamp': int,
        'last_traded_price': int,
        'subscription_mode_val': str,
        'last_traded_quantity': int,
        'average_traded_price': int,
        'volume_trade_for_the_day': int,
        'total_buy_quantity': float,
        'total_sell_quantity': float,
        'open_price_of_the_day': int,
        'high_price_of_the_day': int,
        'low_price_of_the_day': int,
        'closed_price': int,
        'last_traded_timestamp': int,
        'open_interest': int,
        'open_interest_change_percentage': int,
        'upper_circuit_limit': int,
        'lower_circuit_limit': int,
        '52_week_high_price': int,
        '52_week_low_price': int,
        'best_5_buy_data': list,
        'best_5_sell_data': list
    }])

    def __init__(self, home_path: str) -> None:
        self.__home_path = home_path

        self.options_store_key_name = dict()
        self.output_data_files_names = []

    def collect_data(self, options_map: list, name: str) -> None:
        try:
            self.options_map_SCHEMA.validate(options_map)
        except Exception as E:
            raise E

        grouped_by_calls_and_puts = self.__grouping_by_calls_and_puts(
            options_map)

        if name not in self.options_store_key_name:
            self.options_store_key_name[name] = grouped_by_calls_and_puts
        else:
            self.options_store_key_name[name].update(grouped_by_calls_and_puts)

    def print(self) -> None:
        self.__update_menu_file()  # for other programs navigation
        self.__sample_collected_data()  # deleting cases with no pair

        self._push()

    def clear_buffer(self) -> None:
        self.options_store_key_name.clear()
        self.output_data_files_names.clear()

    def _push(self) -> None:
        filenames = self.output_data_files_names
        options_store_keys_list = list(self.options_store_key_name.keys())
        if len(filenames) != len(options_store_keys_list):
            raise Exception(
                'Something goes wrong with making output file names!')

        for filename, key_name in zip(filenames, options_store_keys_list):
            self.__print_by_name(filename, key_name)

    def __print_by_name(self, filename, key_name) -> None:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        text_to_put = f"{current_time}\n"
        for symbol in self.options_store_key_name[key_name].keys():
            text = self._parse_options_data_into_string(
                self.options_store_key_name[key_name][symbol])
            text_to_put = f"{text_to_put}{text}\n"

        name = f"{self.__home_path}{filename}"

        with open(name, "w", encoding="utf-8") as file:
            pass

        with open(name, "w", encoding="utf-8") as file:
            file.write(text_to_put)

    def __update_menu_file(self) -> None:

        path = f"{self.__home_path}menu.txt"
        names_for_storing_data_files = []
        for name in self.options_store_key_name.keys():
            names_for_storing_data_files.append(f"{name}_data.txt")

        with open(path, "w", encoding="utf-8") as file:
            pass

        with open(path, "w", encoding="utf-8") as file:
            text_to_put = ""
            for i, name in enumerate(names_for_storing_data_files):
                if i == (len(names_for_storing_data_files) - 1):
                    text_to_put = f"{text_to_put}{name}"
                else:
                    text_to_put = f"{text_to_put}{name}\n"
            file.write(text_to_put)

        self.output_data_files_names = names_for_storing_data_files

    def __sample_collected_data(self) -> None:
        try:
            self.options_store_key_name_SCHEMA.validate(
                self.options_store_key_name)
        except Exception as E:
            raise Exception

        bad_symbols = []
        for name in self.options_store_key_name.keys():
            for symbol in self.options_store_key_name[name].keys():
                util = list(
                    self.options_store_key_name[name][symbol].keys())
                if len(util) != 2:
                    bad_symbols.append(symbol)

        for name in self.options_store_key_name.keys():
            for symbol in bad_symbols:
                try:
                    del self.options_store_key_name[name][symbol]
                except BaseException:
                    next
                else:
                    next

    def __grouping_by_calls_and_puts(self, options_map) -> dict:
        symbol_indexed_options = dict()

        for option in options_map:
            symbol_full = option['symbol']
            symbol = symbol_full[:len(symbol_full) - 2]
            ce_or_pe_part = symbol_full[len(symbol_full) - 2:]
            if ce_or_pe_part != 'CE' and ce_or_pe_part != 'PE':
                raise Exception(
                    f'{self.__grouping_by_calls_and_puts} get Invalid symbol for option...')

            if symbol in symbol_indexed_options:
                symbol_indexed_options[symbol].update({ce_or_pe_part: option})
            else:
                symbol_indexed_options[symbol] = {ce_or_pe_part: option}

        return symbol_indexed_options

    def _parse_options_data_into_string(self, option_data_ce_pe: dict) -> str:
        pe_data = option_data_ce_pe['PE']
        ce_data = option_data_ce_pe['CE']

        try:
            ce_data['last_traded_price'] = str(
                ce_data['last_traded_price'] / 100)
            pe_data['last_traded_price'] = str(
                pe_data['last_traded_price'] / 100)
        except BaseException:
            pass

        try:
            expiry = pe_data['expiry']
            strike = pe_data['strike'][:5]
        except BaseException:
            pass

        try:
            output = f"expiry:{expiry}/strike:{strike}/"
        except BaseException:
            pass

        list_of_unnecesary_keys = ['expiry', 'strike', 'best_5_buy_data']
        for item in ce_data.items():
            key = item[0]
            value = item[1]
            if key not in list_of_unnecesary_keys:
                output += f"{key}:{value}/"

        for item in pe_data.items():
            key = item[0]
            value = item[1]
            if key not in list_of_unnecesary_keys:
                output += f"{key}:{value}/"

        return output[:len(output) - 1]

    """FOR TEST:"""

    def _test_grouping_by_ce_pe(self, data: dict) -> dict:
        return self.__grouping_by_calls_and_puts(data)

    def _test_sample_data(self, data):
        self.options_store_key_name = data
        self.__sample_collected_data()
        
        output = self.options_store_key_name
        del self.options_store_key_name
        return output
