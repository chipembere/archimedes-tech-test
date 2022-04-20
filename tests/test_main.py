from ast import operator
from pickle import TRUE
import pytest

from src import main


def test_load_json(mock_json_files):
    """test loading json"""
    test_calls_file, _, _, operator_data = mock_json_files
    operator_data == main.load_json(test_calls_file)


def test_load_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        main.load_json("test_calls_file")


def test_split_number(mock_call_data):
    """test splitting phone number"""
    phone_number = mock_call_data["data"][0]["attributes"]["number"]
    country_code, range_prefix, number = main.split_number(phone_number=phone_number)
    assert country_code == "+44"
    assert range_prefix == "1234"
    assert number == "56789"


def test_find_operator(
    mock_operator_data,
):
    """test find operator"""
    operator = main.find_operator(range_prefix="1234", operators=mock_operator_data)
    assert operator == "Vodafone"


def test_find_operator_unknown(
    mock_operator_data,
):
    """test unknown operator"""
    operator = main.find_operator(range_prefix="8234", operators=mock_operator_data)
    assert operator == "Unknown"


def test_generate_risk_score_rounding_up():
    """test risk score generation rounding up"""
    risk_score = main.generate_risk_score(
        risk_score=0.55, green_list=False, red_list=False
    )
    assert risk_score == 0.6


def test_generate_risk_score_rounding_down():
    """test risk score generation rounding down"""
    risk_score = main.generate_risk_score(
        risk_score=0.41, green_list=False, red_list=False
    )
    assert risk_score == 0.4


def test_generate_risk_score_green_list():
    """test risk score generation for a call on the green list and red list"""
    risk_score = main.generate_risk_score(
        risk_score=0.41, green_list=True, red_list=True
    )
    assert risk_score == 0.0


def test_generate_risk_score_red_list():
    """test risk score generation for a call on the red list"""
    risk_score = main.generate_risk_score(
        risk_score=0.41, green_list=False, red_list=True
    )
    assert risk_score == 1.0


def test_generate_csv():
    """end to end to test"""
    pass
