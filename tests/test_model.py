import joblib
from pathlib import Path
import pandas as pd
import json
from ml.training import build_features
from app.config import MODEL_PATH, METADATA_PATH

MODEL_PATH = Path(MODEL_PATH)
METADATA_PATH = Path(METADATA_PATH)
metadata = json.load(open(METADATA_PATH))
required_features = metadata["features"]

# ---------- Test if the model file can be loaded ----------
def test_model_loads():

    model = joblib.load(MODEL_PATH)
    assert model is not None, "The model cannot be load"


# --------- Test if the model can make a prediction ----------
def test_model_prediction():
    
    model = joblib.load(MODEL_PATH)
    raw_input = {
        "X1 transaction date": 2012.667,
        "X2 house age": 10.3,
        "X3 distance to the nearest MRT station": 210.2,
        "X4 number of convenience stores": 5,
        "X5 latitude": 24.98229,
        "X6 longitude": 121.54287
    }

    df = pd.DataFrame([raw_input])
    df = build_features(df)
    df = df[required_features]

    pred = model.predict(df)
    assert isinstance(pred[0], float), "The model cannot make a prediction"