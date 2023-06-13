# Feature Selection for Optasia

Project Description: This project is a Python FastAPI application that serves as an API. It provides three endpoints to interact with the application.
Basically, this project is a link in the chain of a complete ML project and it plays the role of automatic feature extraction for a dataset. 

## Installation

### Easy Install: 
1. Clone the repo: `git clone https://github.com/mordilos/feature_engineering.git`
2. Navigate to the repo dir: `cd feature_engineering`
3. Use the compose.yml to build and run the app: `docker-compose -f compose.yml up`


### Alternative Install:

1. Clone the repository: `git clone https://github.com/mordilos/feature_engineering.git`
2. Navigate to the project directory: `cd feature_engineering`<br /> Now you can choose your next step.
   1. Locally install everything
      1. Create new venv: `python3 -m venv venv_name`
      2. Activate the venv: `source venv_name/bin/activate`
      3. Install the dependencies: `pip install -r requirements.txt`
      4. Start the FastAPI server: `python src/main.py`
      5. Access the endpoints using a web browser or an API client.
      6. You can also run the tests that are in the test folder in `test_main.py`.
   2. Use the Dockerfile to build the image<br />`docker build -t feature_engineering_image .`<br /> and then create and run the container<br />`docker run -d --name fe_container -p 8000:8000 feature_engineering_image`


## Endpoints

### 1. GET /docs

- Description: Returns the built-in swagger documentation.
- URL: `http://localhost:8000/docs`
- Method: `GET`


### 2. GET / (Root)

- Description: Returns all the available endpoints of the app.
- URL: `http://localhost:8000/`
- Method: `GET`
- Response:
  ```json
  {
    "endpoints": [
      "/",
      "/status",
      "/features"
    ]
  }
  ```

### 3. GET /status

- Description: Returns the status of the application.
- URL: `http://localhost:8000/status`
- Method: `GET`
- Response:
  ```json
  {
    "status": "UP"
  }
  ```

### 4. POST /features_file

- Description: Automatic feature extraction for data given in json file. 
- URL: `http://localhost:8000/features_file`
- Method: `POST`
- Request Body:
  ```json
  {
    "file": "<path-to-json-file>",
    "feature_selection": ["keyword1,keyword2"]
  }
  ```
  - `file` (required): Path to the JSON file containing user data.
  - `feature_selection` (optional): List of strings specifying methods to filter the data, [highly_null_features, single_value_features, highly_correlated_features]<br /> (the user can choose between 0 and 3 values) based on https://featuretools.alteryx.com/en/stable/guides/feature_selection.html
- Response:
  ```json
  {
    "feature_matrix": "<extracted-feature-matrix>"
  }
  ```
  - `feature_matrix`: JSON representation of the extracted feature matrix.


### 5. POST /features_json

- Description: Automatic feature extraction for data given in json form. 
- URL: `http://localhost:8000/features_json`
- Method: `POST`
- Request Body:
  ```json
  {
  "data": [
    {
      "customer_ID": "string",
      "loans": [
        {
          "customer_ID": "string",
          "loan_date": "string",
          "amount": "string",
          "fee": "string",
          "loan_status": "string",
          "term": "string",
          "annual_income": "string"
        }
      ]
    }
  ],
  "feature_selection": [
    "string"
  ]
}
  ```
  - `data` (required): data in json format
  - `feature_selection` (optional): List of strings specifying methods to filter the data, [highly_null_features, single_value_features, highly_correlated_features]<br /> (the user can choose between 0 and 3 values) based on https://featuretools.alteryx.com/en/stable/guides/feature_selection.html
- Response:
  ```json
  {
    "feature_matrix": "<extracted-feature-matrix>"
  }
  ```
  - `feature_matrix`: JSON representation of the extracted feature matrix.

## Example

1. Start the FastAPI server.
2. Open a web browser or an API client.
3. Go to `http://localhost:8000/docs` for the built-in swagger documentation. From there you can test all the other endpoints.
4. Send a GET request to `http://localhost:8000/` to get all available endpoints.
5. Send a GET request to `http://localhost/status:8000` to check the application status.
6. Send a POST request to `http://localhost/features:8000` with a JSON body containing the path to the data file and optional keywords to extract features.<br />
    CLI example that uses all the feature selection algorithms:<br />`curl -X 'POST' \`<br />`'http://localhost:8000/features' \`<br />`-H 'accept: application/json' \`<br />`-H 'Content-Type: multipart/form-data' \`<br />`-F 'file=@cvas_data.json;type=application/json' \`<br />`-F 'feature_selection=highly_null_features,single_value_features,highly_correlated_features'`
7. Receive the extracted feature matrix in the response.

## License

[MIT License](https://opensource.org/licenses/MIT)