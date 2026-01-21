import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pathlib import Path
import joblib
import json
from datetime import datetime

MODEL_VERSION = datetime.now().strftime("v%Y%m%d%H%M%S")
MODEL_PATH = f"ml/model_{MODEL_VERSION}.joblib"
METADATA_PATH = f"ml/metadata_{MODEL_VERSION}.json"
DATA_PATH = Path("data/Real estate.csv")

def build_features(df):
    df = df.copy()
    df["house_age_squared"] = df["X2 house age"] ** 2
    return df

def main():
    df = pd.read_csv(DATA_PATH)

    raw_features = ["X1 transaction date", "X2 house age", "X3 distance to the nearest MRT station",
                    "X4 number of convenience stores", "X5 latitude", "X6 longitude"]

    X = build_features(df[raw_features])
    y = df["Y house price of unit area"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    metadata = {"features": list(X.columns)}
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f)

    y_test_pred = model.predict(X_test)
    test_mse = mean_squared_error(y_test, y_test_pred)
    print(f"Test MSE: {test_mse:.3f}")

if __name__ == "__main__":
    main()
