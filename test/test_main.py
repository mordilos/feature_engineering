import json.decoder

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
input_file = "cvas_data.json"


def test_index():
    all_routes = ['/features', '/status', '/']
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"endpoints": all_routes}


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_create_features_no_params():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": []}
    test_response = open('test_response.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features",
                           files=files,
                           data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_highly_null():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_null_features']}
    test_response = open('test_response_highly_null.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_single_value():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['single_value_features']}
    test_response = open('test_response_single_value.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_highly_correlated():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_correlated_features']}
    test_response = open('test_response_highly_correlated.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_all():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_null_features,single_value_features,highly_correlated_features']}
    test_response = open('test_response_all.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json
