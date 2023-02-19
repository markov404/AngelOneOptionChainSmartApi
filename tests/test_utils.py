
import pytest

from ..components.utlis import (
    make_token_list_for_web_socket as func1,
    make_set_of_option_names as func2,
    check_on_error as func3,
    sort_by_name_of_option_and_split_result_on_chunks as func4
)


# testing func1
def test_one_positive():
    t_inp1 = [
        {'token': '123'},
        {'token': '3213'},
        {'token': '2132'}
    ]
    t_out1 = ['123', '3213', '2132']

    assert func1(t_inp1) == t_out1


def test_one_negative():
    t_inp2 = [{'token': '1232'}, {''}]
    t_out2 = ['1232']

    t_inp3 = [
        {'token': 1232},
        {''},
        {'token': '4444'}
    ]
    t_out3 = ['1232', '4444']

    t_inp4 = []
    t_out4 = []

    assert func1(t_inp2) == t_out2
    assert func1(t_inp3) == t_out3
    assert func1(t_inp4) == t_out4


# testing func2
def test_two_positive():
    t_inp1 = [
        {'name': 'SLOWLU'},
        {'name': 'FIDGI'},
        {'name': ''}
    ]
    t_out2 = set(['SLOWLU', 'FIDGI'])

    assert func2(t_inp1) == t_out2


def test_two_negative():
    t_inp1 = [
        {'name': 3453},
        {'name': 'FIDGI'},
        {'name': ''}
    ]
    t_out1 = set(['FIDGI'])

    t_inp2 = [{}, {'name': 66.4234}, {'name': 'ORIGIN'}]
    t_out2 = set(['ORIGIN'])

    assert func2(t_inp1) == t_out1
    assert func2(t_inp2) == t_out2


# testing func3
def test_three_positive():
    t_inp1 = {"errorCode": "Blabla", "FAMILYGUY": True}
    t_inp2 = {"FAMILY": "LALALA"}

    with pytest.raises(Exception) as e_info:
        func3(t_inp1)

    assert func3(t_inp2) is None


def test_three_negative():
    t_inp1 = 13123
    with pytest.raises(Exception) as e_info:
        func3(t_inp1)


# testing func4
def test_four_positive():
    t_inp1_1 = [
        {'name': 'OPTIDX'},
        {'name': 'SMARTAPI'},
        {'name': 'JOHNSON'},
        {'name': 'OPTIDX'}
    ]
    t_inp1_2 = [
        'OPTIDX',
        'SMARTAPI',
        'JOHNSON',
        'OPTIDX'
    ]
    t_outp1 = {
        'OPTIDX': [[{'name': 'OPTIDX'}, {'name': 'OPTIDX'}]],
        'SMARTAPI': [[{'name': 'SMARTAPI'}]],
        'JOHNSON': [[{'name': 'JOHNSON'}]]
    }

    assert func4(t_inp1_1, t_inp1_2) == t_outp1


def test_four_negative():
    t_inp1_1 = [
        {},
        {'name': 'SMARTAPI'},
        {'name': 'JOHNSON'},
        {'name': 'OPTIDX'}
    ]
    t_inp1_2 = [
        123,
        'SMARTAPI',
        'JOHNSON',
        'OPTIDX'
    ]
    with pytest.raises(Exception) as e_info:
        func4(t_inp1_1, t_inp1_2)
