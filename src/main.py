import json
import logging
from typing import List, Optional

import featuretools as ft
import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException, APIRouter, Form, File
from pydantic import BaseModel, ValidationError, parse_obj_as
from woodwork.logical_types import Categorical, Boolean

app = FastAPI()
router = APIRouter()


def init_logger():
    logger = logging.getLogger("feature engineering app")
    logger.setLevel("DEBUG")  # INFO, WARNING, CRITICAL, DEBUG, ERROR
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_routes(routes):
    all_routes = []
    reserved_routes = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    for route in routes:
        if route.path not in reserved_routes:
            if route.name is not None:
                all_routes.append(route.path)
    return all_routes


class Loan(BaseModel):
    customer_ID: str
    loan_date: str
    amount: str
    fee: str
    loan_status: str
    term: str
    annual_income: str

    def to_dict(self):
        return {
            "customer_ID": self.customer_ID,
            "loan_date": self.loan_date,
            "amount": self.amount,
            "fee": self.fee,
            "loan_status": self.loan_status,
            "term": self.term,
            "annual_income": self.annual_income
        }


class UserData(BaseModel):
    customer_ID: str
    loans: list[Loan]

    def get_customer_id(self):
        return self.customer_ID

    def get_loans(self):
        return [loan.to_dict() for loan in self.loans]


class UsersData(BaseModel):
    __root__: list[UserData]

    def get_customer_df(self):
        return pd.DataFrame([user_data.get_customer_id() for user_data in self.__root__], columns=["customer_ID"])

    def get_loans_df(self):
        return pd.DataFrame([loan for user_data in self.__root__ for loan in user_data.get_loans()]). \
            reset_index().rename(columns={"index": "loan_ID"})


def feature_eng(customers_df: pd.DataFrame,
                loans_df: pd.DataFrame,
                feature_selection: List[str] = None):
    logger.debug(f"Creating the Entity Set 'customer_data'")
    es = ft.EntitySet(id="customer_data")
    logger.debug(f"Adding the dataframe 'customers' to the 'customer_data' Entity Set")
    es = es.add_dataframe(dataframe_name="customers", dataframe=customers_df, index="customer_ID")
    logger.debug(f"Adding the dataframe 'loans' to the 'customer_data' Entity Set")
    es = es.add_dataframe(dataframe_name="loans", dataframe=loans_df, index="loan_ID",
                          logical_types={"term": Categorical, "loan_status": Boolean},
                          time_index="loan_date")
    logger.debug(f"Adding the relationship of the two dataframes to the 'customer_data' Entity Set")
    es = es.add_relationship("customers", "customer_ID", "loans", "customer_ID")

    logger.debug(f"Initiating the Deep Feature Synthesis procedure..")
    feature_matrix, feature_defs = ft.dfs(entityset=es,
                                          target_dataframe_name="customers",
                                          max_depth=2,
                                          verbose=0,
                                          n_jobs=1)
    if feature_selection:
        for mode in feature_selection:
            if mode == 'highly_null_features':
                logger.debug(f"Feature Selection with 'highly_correlated_features'")
                feature_matrix, feature_defs = ft.selection.remove_highly_null_features(feature_matrix=feature_matrix,
                                                                                        features=feature_defs)
            elif mode == 'single_value_features':
                logger.debug(f"Feature Selection with 'single_value_features'")
                feature_matrix, feature_defs = ft.selection.remove_single_value_features(feature_matrix=feature_matrix,
                                                                                         features=feature_defs)
            elif mode == 'highly_correlated_features':
                logger.debug(f"Feature Selection with 'highly_correlated_features'")
                feature_matrix, feature_defs = ft.selection.remove_highly_correlated_features(
                    feature_matrix=feature_matrix,
                    features=feature_defs)
    logger.debug(f"Deep Feature Synthesis procedure DONE")
    logger.info(f"Number of features created: {len(feature_defs)}")
    logger.debug(f"Features created: {feature_defs}")
    fm_json = feature_matrix.to_json(orient='index')
    parsed = json.loads(fm_json)
    logger.debug(f"The parsed Features Matrix: \n{parsed}")
    return json.dumps(parsed, indent=4)


@router.get("/")
async def index():
    logger.info(f"Get all the endpoints of this API")
    return {"endpoints": all_routes}


@app.post("/features_file")
async def create_features_file(file: UploadFile = File(...),
                               feature_selection: Optional[List[str]] = Form(None)):
    logger.info(f"Create Features from given data.")
    logger.info(f"Started creating features...")
    logger.info(f"Feature Selection method requested: {feature_selection}")

    if file is None:
        logger.info(f"No file provided...")
        raise HTTPException(status_code=400, detail="No file received")
    if feature_selection:
        feature_selection = feature_selection[0].split(",")
    try:
        logger.debug(f"Reading file..")
        json_file = json.loads(file.file.read())
        logger.debug(f"Parsing file...")
        parsed_data = parse_obj_as(obj=json_file['data'], type_=UsersData)
        # check if duplicate id
    except ValidationError as error:
        logger.error(f"{error}")
        raise HTTPException(status_code=400, detail=str(error))

    logger.debug(f"Creating the customers dataframe")
    customers_df = parsed_data.get_customer_df()
    logger.debug(f"Creating the loans dataframe")
    loans_df = parsed_data.get_loans_df()

    logger.debug(f"Feature engineering step")
    features_json = feature_eng(customers_df=customers_df,
                                loans_df=loans_df,
                                feature_selection=feature_selection)
    logger.info(f"Created new features...")
    return features_json


@app.post("/features_json")
async def create_features_json(data: UsersData,
                               feature_selection: Optional[List[str]]):
    logger.info(f"Create Features from given data.")
    logger.info(f"Started creating features...")

    if data is None:
        logger.info(f"No data provided...")
        raise HTTPException(status_code=400, detail="No data received")
    logger.debug(f"Creating the customers dataframe")
    customers_df = data.get_customer_df()
    logger.debug(f"Creating the loans dataframe")
    loans_df = data.get_loans_df()

    logger.debug(f"Feature engineering step")
    features_json = feature_eng(customers_df=customers_df,
                                loans_df=loans_df,
                                feature_selection=feature_selection)
    logger.info(f"Created new features...")
    return features_json


@app.get("/status")
async def status():
    logger.info(f"Get the status of the app")
    logger.info(f"status: UP")
    return {"status": "UP"}


logger = init_logger()
app.include_router(router)
all_routes = get_routes(app.routes)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
