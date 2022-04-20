import os
import json
import pytest

call_data = {
    "data": [
        {
            "type": "call",
            "id": "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b",
            "attributes": {
                "date": "2020-10-12T07:20:50.52Z",
                "riskScore": 0.431513435443,
                "number": "+44123456789",
                "greenList": True,
                "redList": False,
            },
        },
        {
            "type": "call",
            "id": "8f1b1354-26d2-4e16-9582-9156a0d9a5de",
            "attributes": {
                "date": "2019-10-12T07:20:50.52Z",
                "riskScore": 0.123444,
                "number": "+44123456789",
                "greenList": False,
                "redList": True,
            },
        },
    ]
}


operator_data = {
    "data": [
        {
            "type": "operator",
            "id": "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b",
            "attributes": {"prefix": "1000", "operator": "Vodafone"},
        },
        {
            "type": "operator",
            "id": "8f1b1354-26d2-4e16-9582-9156a0d9a5de",
            "attributes": {"prefix": "2000", "operator": "EE"},
        },
    ]
}


@pytest.fixture(scope="function")
def mock_call_data():
    return call_data


@pytest.fixture(scope="function")
def mock_operator_data():
    return operator_data


@pytest.fixture(scope="function")
def mock_json_files(tmp_path):
    temp_dir = tmp_path / "sub"
    temp_dir.mkdir()
    os.chdir(temp_dir)
    test_calls_file = temp_dir / "test_calls.json"
    with open("test_calls.json", "w") as outfile:
        json.dump(call_data, outfile)

    test_operator_file = temp_dir / "test_operator.json"
    with open("test_operator.json", "w") as outfile:
        json.dump(call_data, outfile)
    yield str(test_calls_file), call_data, str(test_operator_file), operator_data
