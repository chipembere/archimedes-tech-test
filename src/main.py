import os
import json
import errno


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
