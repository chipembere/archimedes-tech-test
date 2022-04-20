import os
import json
import errno
import decimal
import pandas as pd
import datetime as dt


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
        operators_list = operators.get("data")
        if len(operators_list) > 0:
            r = 0
            for operator in operators_list:
                if operator["attributes"]["prefix"][0] == range_prefix[0]:
                    return operator["attributes"]["operator"]
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


if __name__ == "__main__":
    calls_data_path = "data/calls.json"
    operators_data_path = "data/operators.json"

    calls_data = load_json(file_path=calls_data_path)
    operators_data = load_json(file_path=operators_data_path)

    enriched_calls: list = []
    for call in calls_data["data"]:
        enriched_call: dict = {}
        id = call.get("id")
        phone_number = (
            "Withheld"
            if not call.get("attributes").get("number")
            else call.get("attributes").get("number")
        )
        risk_score = call.get("attributes").get("riskScore")
        green_list = call.get("attributes").get("greenList")
        red_list = call.get("attributes").get("redList")
        country_code, range_prefix, number = split_number(phone_number=phone_number)
        operator = (
            "Unknown"
            if phone_number == "Withheld"
            else find_operator(range_prefix=range_prefix, operators=operators_data)
        )
        risk_score = generate_risk_score(
            risk_score=risk_score, green_list=green_list, red_list=red_list
        )
        date = dt.datetime.strptime(
            call.get("attributes").get("date"), "%Y-%m-%dT%H:%M:%SZ"
        ).date()
        enriched_call["id"] = id
        enriched_call["date"] = date
        enriched_call["number"] = phone_number
        enriched_call["operator"] = operator
        enriched_call["riskScore"] = risk_score
        enriched_calls.append(enriched_call)

    df = pd.DataFrame(enriched_calls)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", ascending=True)
    print(df)
    df.to_csv("data/enriched_calls.csv")
