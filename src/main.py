import os
import json
import errno
import decimal


def load_json(file_path: str) -> dict:
    """open and load json data
    Parameters:
        file_path (str): path to json file
    Returns:
        dict: the json string is converted into a dictionary
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def split_number(phone_number: str) -> tuple:
    """split phone number and return the fragments
    Parameters:
        phone_number (str): phone in number as a string.
    Returns:
        (tuple): a tuple of strings
    """
    try:
        country_code, range_prefix, number = (
            phone_number[:3],
            phone_number[3:7],
            phone_number[7:],
        )
        return country_code, range_prefix, number
    except Exception as e:
        print(e)


def find_operator(range_prefix: str, operators: list) -> str:
    """using the range prefix find the operator of a number
    from a list of operators dictionaries.

    Parameters:
        range_prefix (str): range prefix from phone number
        operators (list): list of operators dictionaries
    Return:
        operator (str): the name of the operator if found
        'Unknowm' (str): if operator is not found
    """
    try:
        for operator in operators["data"]:
            if operator["attributes"]["prefix"][0] == range_prefix[0]:
                return operator["attributes"]["operator"]
            else:
                return "Unknown"

    except Exception as e:
        print(e)


def generate_risk_score(risk_score: float, green_list: bool, red_list: bool):
    """Generate a risk score, depending on wether a call is on the red or green list
    and rounding the original riskScore value if the call is not on either list.

    Parameters:
        risk_score (float): call risk score
        green_list (bool): if call is on the green list
        red_list (bool): if call is on the red list
    Returns:
        risk_score (float): a revised risk score
    """
    # being on the green list has precedence over red list, meaning if a call is on both lists its == 0.0
    if green_list:
        return 0.0
    elif red_list:
        return 1.0
    elif red_list and not green_list:
        return 1.0
    else:
        return float(
            decimal.Decimal(str(risk_score)).quantize(
                decimal.Decimal("1.0"), rounding=decimal.ROUND_HALF_EVEN
            )
        )
    # if a call is on a red list only its risk score is 1.0
    # if the call is on the green list only == 0.0
    # if call not on either red or green list;
    # round everything from half up to 1 decimal point and all values below half are round down
