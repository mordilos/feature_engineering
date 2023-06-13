# Feature Selection for Optasia

Project Description: This project is a Python FastAPI application that serves as an API. It provides three endpoints to interact with the application.
Basically, this project is a link in the chain of a complete ML project and it plays the role of automatic feature extraction for a dataset. 

## Installation

### 1. Download the project (Github)

1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Navigate to the project directory: `cd your-repo`.<br /> Now you can choose your next step.
   1. Install the dependencies: `pip install -r requirements.txt`
   2. Use the Dockerfile to build the image<br />`docker build -t feature_engineering_image .`<br /> and then create and run the container<br />`docker run -d --name fe_container -p 8000:8000 feature_engineering_image`
   3. Use the compose.yml to build the container.<br /> `docker-compose build`<br />then start it<br /> `docker-compose up`

### 2. Download the Container (Docker Hub)
  1. 

## Usage (only if you choose not to run the app in a container)

1. Activate the venv: `source bin/activate`
2. Start the FastAPI server: `python src/main.py`
2. Access the endpoints using a web browser or an API client.

## Endpoints

### 1. GET / (Root)

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

### 2. GET /status

- Description: Returns the status of the application.
- URL: `http://localhost:8000/status`
- Method: `GET`
- Response:
  ```json
  {
    "status": "UP"
  }
  ```

### 3. POST /features

- Description: Automatic feature extraction for data given in json file. 
- URL: `http://localhost:8000/features`
- Method: `POST`
- Request Body:
  ```json
  {
    "file": "<path-to-json-file>",
    "feature_selection": ["keyword1,keyword2"]
  }
  ```
  - `file` (required): Path to the JSON file containing user data.
  - `feature_selection` (optional): List of strings specifying methods to filter the data, [highly_null_features, single_value_features, highly_correlated_features] (the user can choose between 0 and 3 values) based on https://featuretools.alteryx.com/en/stable/guides/feature_selection.html
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
3. Send a GET request to `http://localhost/` to get all available endpoints.
4. Send a GET request to `http://localhost/status` to check the application status.
5. Send a POST request to `http://localhost/features` with a JSON body containing the path to the data file and optional keywords to extract features.
6. Receive the extracted feature matrix in the response.

## License

[MIT License](https://opensource.org/licenses/MIT)