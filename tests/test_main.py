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
    

def test_split_number():
    """split phone number and return the fragments
    Parameters:
        phone_number (str): phone in number as a string.
    Returns:
        (tuple): the parts of number as tuple
    """
    pass


def test_find_operator():
    """using the range prefix find the operator of a number
    from a list of operators in dictionary.

    Parameters:
        range_prefix (str): range prefix from phone number
    Return:
        operator (str): the name of the operator if found
        'unknowm' (str): if operator is not found
    """
    pass


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
