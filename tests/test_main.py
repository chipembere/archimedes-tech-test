from ast import operator
import pytest

from src import main


def test_load_json(mock_json_files):
    """open and load json data
    Parameters:
        file_path (str): path to json file
    Returns:
        dict: the json string is converted into a dictionary
    """
    test_calls_file, call_data, test_operator_file, operator_data = mock_json_files
    operator_data == main.load_json(test_calls_file)


def test_load_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        main.load_json("test_calls_file")


def test_split_number(mock_call_data):
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


def test_generate_risk_score():
    """Generate a risk score, depending on wether a call is on the red or green list
    and rounding the original riskScore value if the call is not on either list.

    Parameters:
        risk_score (float): call risk score
        green_list (bool): if call is on the green list
        red_list (bool): if call is on the red list
    Returns:
        risk_score (float): a revised risk score
    """
    # being on the green list has precedence over red list, meaning if a call is on both lists its == 0
    # if a call is on a red list only its risk score is 1.0
    # if the call is on the green list only == 0.0
    # if call not on either red or green list;
    # roundd everything from half up to 1 decimal point and all values below half are round down
    pass


def test_generate_csv():
    """end to end to test"""
    pass
