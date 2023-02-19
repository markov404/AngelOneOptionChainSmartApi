
import pytest
from ..components.output_processor import OutputProcessor

path = 'E:\\projects\\venv\\Scripts\\work\\AngeloneAppV2'


def test_one_positive():
    proc = OutputProcessor(path)

    t_inp1 = {
        'CE': {
            'expiry': '18MAR22',
            'strike': '123546.000',
            'last_traded_price': 45677,
            'mol': '6579404',
        },
        'PE': {
            'expiry': '18MAR22',
            'strike': '123546.000',
            'last_traded_price': 789852,
            'val': '568379'
        }
    }

    p1 = "expiry:18MAR22/strike:12354/last_traded_price:456.77/mol:6579404"
    p2 = "/last_traded_price:7898.52/val:568379"
    t_out1 = p1 + p2

    assert proc._parse_options_data_into_string(t_inp1) == t_out1


def test_one_negative():
    proc = OutputProcessor(path)

    t_inp1 = {
        'CE': {
            'expiry': '18MAR22',
            'strike': '123546.000',
            'mol': '6579404',
        },
        'PE': {
            'expiry': '18MAR22',
            'strike': '123546.000',
            'val': '568379',
        }
    }

    p1 = "expiry:18MAR22/strike:12354/mol:6579404"
    p2 = "/val:568379"
    t_out1 = p1 + p2

    assert proc._parse_options_data_into_string(t_inp1) == t_out1


def test_two_positive():
    proc = OutputProcessor(path)

    t_inp1 = [
        {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
        {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'},
        {'symbol': 'SYMBOL123PE', 'LOK': 555}
    ]

    t_out1 = {
        'SYMBOL123': {
            'CE': {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
            'PE': {'symbol': 'SYMBOL123PE', 'LOK': 555}
        },
        'SYMBOL125': {
            'PE': {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'}
        }
    }

    assert proc._test_grouping_by_ce_pe(t_inp1) == t_out1


def test_two_negative():
    proc = OutputProcessor(path)

    t_inp1 = [
        {'symbol': 'SYMBOL123', 'FORK': 'LUCK'},
        {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'},
        {'symbol': 'SYMBOL123PE', 'LOK': 555}
    ]

    t_out1 = {
        'SYMBOL123': {
            'CE': {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
            'PE': {'symbol': 'SYMBOL123PE', 'LOK': 555}
        },
        'SYMBOL125': {
            'PE': {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'}
        }
    }

    with pytest.raises(Exception) as e_info:
        proc._test_grouping_by_ce_pe(t_inp1)


def test_three_positive():
    proc = OutputProcessor(path)

    t_inp1 = {
        'BANKNIFTY': {
            'SYMBOL123': {
                'CE': {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
                'PE': {'symbol': 'SYMBOL123PE', 'LOK': 555}
            },
            'SYMBOL125': {
                'PE': {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'}
            }
        },
        'NIFTY': {
            'SYMBOL127': {
                'PE': {'symbol': 'SYMBOL127PE', 'TOK': 777}
            },
            'SYMBOL127': {
                'CE': {'symbol': 'SYMBOL127CE', 'CHICHA': 'HUICHICHA'},
                'PE': {'symbol': 'SYMBOL127PE', 'LALAL': '127'}
            } 
        }
    }

    t_out1 = {
        'BANKNIFTY': {
            'SYMBOL123': {
                'CE': {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
                'PE': {'symbol': 'SYMBOL123PE', 'LOK': 555}
            }
        },
        'NIFTY': {
            'SYMBOL127': {
                'CE': {'symbol': 'SYMBOL127CE', 'CHICHA': 'HUICHICHA'},
                'PE': {'symbol': 'SYMBOL127PE', 'LALAL': '127'}
            } 
        }
    }

    assert proc._test_sample_data(t_inp1) == t_out1


def test_three_negative():
    proc = OutputProcessor(path)

    # below unvalid schema
    t_inp1 = {
        'BANKNIFTY': {
            'SYMBOL123': {
                'CE': {'symbol': 'SYMBOL123CE', 'FORK': 'LUCK'},
                'PE': {'symbol': 'SYMBOL123PE', 'LOK': 555}
            },
            'SYMBOL125': {
                'PE': {'symbol': 'SYMBOL125PE', 'MORZHA': 'CHICH'}
            }
        },
        'NIFTY': {
            'SYMBOL127': {
                'SOME': {'symbol': 'SYMBOL127PE', 'TOK': 777}
            },
            'SYMBOL127': {
                'DOPE': {'symbol': 'SYMBOL127CE', 'CHICHA': 'HUICHICHA'},
                'GUYS': {'symbol': 'SYMBOL127PE', 'LALAL': '127'}
            } 
        }
    }

    with pytest.raises(Exception) as e_info:
        proc._test_sample_data(t_inp1)


def test_four_positive():
    name = 'NIFTY'
    options_map = [{
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
    }]
    proc = OutputProcessor(path)

    assert proc.collect_data(options_map, name) == None

def test_four_positive():
    name = 'NIFTY'
    options_map = [{
        'token': '47338',
        'volume_trade_for_the_day': 100,
        'total_buy_quantity': 'sdf',
        'sdf': 2250.0,
        'open_price_of_the_day': 32525,
        'high_price_of_the_day': 32525,
        'low_price_of_the_day': 32525,
        'sdfs': 26205,
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
    }]
    proc = OutputProcessor(path)

    with pytest.raises(Exception) as e_info:
        proc.collect_data(options_map, name)
