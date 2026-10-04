from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import List, Dict, Any

# 1. Initialize FastAPI app
app = FastAPI(title="Real-Time Network Intrusion Detection API", version="1.0")

# 2. Load ML Artifacts on startup
# We use relative paths assuming we run the server from the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

try:
    print("Loading ML artifacts into memory...")
    preprocessor = joblib.load(os.path.join(MODELS_DIR, "preprocessor.joblib"))
    mi_selector = joblib.load(os.path.join(MODELS_DIR, "mi_selector.joblib"))
    xgb_binary = joblib.load(os.path.join(MODELS_DIR, "xgboost_binary.joblib"))
    print("All artifacts loaded successfully!")
except Exception as e:
    print(f"Error loading artifacts: {e}")

# 3. Define the Input Data Schema
# We accept a list of dictionaries to allow batch predictions
class FlowRequest(BaseModel):
    flows: List[Dict[str, Any]]

@app.get("/")
def health_check():
    return {"status": "Active", "message": "IDS API is running."}

@app.post("/predict")
def predict_flows(request: FlowRequest):
    try:
        # Convert incoming JSON into a Pandas DataFrame
        df_input = pd.DataFrame(request.flows)
        
        # Ensure we don't have target variables or IDs in the input
        cols_to_drop = [col for col in ['id', 'label', 'attack_cat'] if col in df_input.columns]
        if cols_to_drop:
            df_input = df_input.drop(columns=cols_to_drop)

        # Step A: Preprocess (Scale & Encode)
        X_processed = preprocessor.transform(df_input)
        
        # Convert back to DataFrame to preserve feature names for SelectKBest
        cat_cols = ['proto', 'service', 'state']
        num_cols = df_input.select_dtypes(include=['int64', 'float64']).columns.tolist()
        feature_names = num_cols + list(preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols))
        X_processed_df = pd.DataFrame(X_processed, columns=feature_names)

        # Step B: Feature Selection (Mutual Information)
        X_selected = mi_selector.transform(X_processed_df)

        # Step C: Prediction
        predictions = xgb_binary.predict(X_selected)
        probabilities = xgb_binary.predict_proba(X_selected)

        # Format the response
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "flow_index": i,
                "prediction": "Attack" if pred == 1 else "Normal",
                "confidence": float(max(probabilities[i]))
            })
            
        return {"predictions": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")