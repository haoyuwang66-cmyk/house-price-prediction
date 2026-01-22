from pathlib import Path
MODEL_PATH = "ml/model_v20260122120821.joblib" # Update the model path with model that you want to deploy
METADATA_PATH = str(MODEL_PATH).replace("model", "metadata").replace(".joblib", ".json")