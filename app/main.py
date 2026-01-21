from fastapi import FastAPI
from app.schemas import HouseFeatures
from pathlib import Path
from datetime import date
import joblib
import logging
import pandas as pd
from app.config import MODEL_PATH, METADATA_PATH
import json
from ml.training import build_features

MODEL_PATH = Path(MODEL_PATH)
METADATA_PATH = Path(METADATA_PATH)
metadata = json.load(open(METADATA_PATH))
required_features = metadata["features"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="House Price Prediction Service")

model = joblib.load(MODEL_PATH)

def date_to_float(d):
    year_start = date(d.year, 1, 1)
    year_end = date(d.year + 1, 1, 1)
    return d.year + (d - year_start).days / (year_end - year_start).days

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(features: HouseFeatures):
    raw_input = {
        "X1 transaction date": date_to_float(features.transaction_date),
        "X2 house age": features.house_age,
        "X3 distance to the nearest MRT station": features.distance_to_the_nearest_MRT_station,
        "X4 number of convenience stores": features.number_of_convenience_stores,
        "X5 latitude": features.latitude,
        "X6 longitude": features.longitude
    }
    
    logger.info(f"Request: {raw_input}")
    df = pd.DataFrame([raw_input])
    df = build_features(df)
    df = df[required_features]
    prediction = model.predict(df)[0]
    logger.info(f"Response: {prediction}")
    return {"predicted_price": prediction}