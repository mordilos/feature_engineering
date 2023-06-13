import json.decoder

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
input_file = "cvas_data.json"


def test_index():
    all_routes = ['/features_file', '/features_json', '/status', '/']
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"endpoints": all_routes}


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}


def test_create_features_file_no_params():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": []}
    test_response = open('test_response.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_file",
                           files=files,
                           data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_file_highly_null():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_null_features']}
    test_response = open('test_response_highly_null.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_file", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_file_single_value():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['single_value_features']}
    test_response = open('test_response_single_value.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_file", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_file_highly_correlated():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_correlated_features']}
    test_response = open('test_response_highly_correlated.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_file", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_file_all():
    files = {"file": (input_file, open(input_file, "rb"))}
    data = {"feature_selection": ['highly_null_features,single_value_features,highly_correlated_features']}
    test_response = open('test_response_all.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_file", files=files, data=data)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_json_no_params():
    files = {"data": json.loads(open(input_file, "rb").read())['data'], "feature_selection": []}
    test_response = open('test_response.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_json", json=files)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_json_highly_null():
    files = {"data": json.loads(open(input_file, "rb").read())['data'], "feature_selection": ['highly_null_features']}
    test_response = open('test_response_highly_null.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_json", json=files)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_json_single_value():
    files = {"data": json.loads(open(input_file, "rb").read())['data'], "feature_selection": ['single_value_features']}
    test_response = open('test_response_single_value.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_json", json=files)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_json_highly_correlated():
    files = {"data": json.loads(open(input_file, "rb").read())['data'], "feature_selection": ['highly_correlated_features']}
    test_response = open('test_response_highly_correlated.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_json", json=files)

    assert response.status_code == 200
    assert response.json() == test_response_json


def test_create_features_json_all():
    files = {"data": json.loads(open(input_file, "rb").read())['data'], "feature_selection": ['highly_correlated_features','single_value_features', 'highly_correlated_features']}
    test_response = open('test_response_all.json')
    test_response_json = json.dumps(json.load(test_response), indent=4)

    response = client.post("/features_json", json=files)

    assert response.status_code == 200
    assert response.json() == test_response_json
