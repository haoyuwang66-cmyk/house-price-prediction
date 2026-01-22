# House Price Prediction Service

## Description
This project is a proof-of-concept REST API for predicting real estate prices.  
It uses a linear regression model trained on historical real estate data.  
The API is built with FastAPI and supports input validation using Pydantic.

The project includes:
- Model training and saving with feature metadata.
- REST API for prediction with logging.
- Automated tests for model prediction and API endpoints.
- CI workflow for testing the deployed model.


## Requirements
- Python 3.8+
- pip
- Dependencies (install via `requirements.txt`):

## Setup

### 1. Clone the repository
git clone https://github.com/haoyuwang66-cmyk/house-price-prediction.git

cd house-price-service

### 2. Create and activate a virtual environment
python3 -m venv venv

source venv/bin/activate

### 3. Install dependencies
pip install --upgrade pip

pip install -r requirements.txt

### 4. Train the model (optional, if you want to retrain it)
In ml/training.py, in def main(), modify the list raw_features to include the features that you want to use. In 
def build_features(), add the features that you want to build or delete existing features.

python ml/training.py

### 5. Select a model that you want to deploy (optional, if you want to update the model used in RESTAPI)
Select an exsiting model that you want to use and copy the relative path, in app/config.py, modify the MODEL_PATH with the path copied.

### 6. Run the API
uvicorn app.main:app --reload

Health check:

GET /health

Prediction:

POST /predict with JSON payload:

{
  "transaction_date": "2013-01-01",
  "house_age": 10.3,
  "distance_to_the_nearest_MRT_station": 210.2,
  "number_of_convenience_stores": 5,
  "latitude": 24.98229,
  "longitude": 121.54287
}

Or try with http://127.0.0.1:8000/docs

Terminate the Uvicorn app: CTRL + C

### 7. Run Tests

Model tests

pytest tests/test_model.py --disable-warnings -q

API tests

pytest tests/test_api.py --disable-warnings -q