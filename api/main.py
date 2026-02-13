import sys
import os
import joblib
import pandas as pd
import numpy as np
import time
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime

# --- 1. SETUP LOGGING (The "Black Box" Recorder) ---
# We will save every single prediction to a CSV file for drift analysis
LOG_FILE = "monitoring_logs.csv"
logging.basicConfig(filename="system_events.log", level=logging.INFO)

# Create the CSV header if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,latency_ms,flow,ph,conductivity,cod,prediction,status\n")

# --- 2. SETUP PATHS & LOAD MODEL ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "bod_predictor.joblib")

app = FastAPI(
    title="Wastewater BOD Predictor (Monitored)",
    description="Real-time Soft Sensor with Drift Detection & Latency Tracking",
    version="1.1.0"
)

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from: {MODEL_PATH}")
except FileNotFoundError:
    print(f"CRITICAL: Model not found at {MODEL_PATH}")
    model = None

# --- 3. DATA SCHEMA ---
class WastewaterReading(BaseModel):
    date: str
    flow: float
    ph: float
    conductivity: float
    cod: float

# --- 4. HELPER: FEATURE ENGINEERING ---
def preprocess_input(data: WastewaterReading) -> pd.DataFrame:
    try:
        dt = datetime.strptime(data.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    month = dt.month
    sin_month = np.sin(2 * np.pi * month / 12)
    cos_month = np.cos(2 * np.pi * month / 12)
    
    return pd.DataFrame([{
        'Q_E_Input_Flow': data.flow,
        'PH_E_Input_pH': data.ph,
        'COND_E_Input_Conductivity': data.conductivity,
        'DQO_E_Input_COD': data.cod,
        'sin_month': sin_month,
        'cos_month': cos_month
    }])

# --- 5. THE MONITORING MIDDLEWARE (New!) ---
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate Latency
    process_time = (time.time() - start_time) * 1000 # Convert to ms
    
    # Log system health (Assignment Requirement: Service Latency)
    logging.info(f"Path: {request.url.path} | Status: {response.status_code} | Latency: {process_time:.2f}ms")
    
    return response

# --- 6. PREDICTION ENDPOINT (With Data Logging) ---
@app.post("/predict")
def predict_bod(reading: WastewaterReading):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    start_cpu = time.process_time()
    
    # A. Prediction Pipeline
    features_df = preprocess_input(reading)
    prediction_log = model.predict(features_df)
    prediction_real = np.expm1(prediction_log)[0]
    
    latency = (time.process_time() - start_cpu) * 1000
    
    status = "Normal" if prediction_real < 400 else "Shock Load Warning ⚠️"

    # B. SAVE DATA FOR DRIFT MONITORING (Assignment Requirement)
    # We append this request to our "Black Box" CSV
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()},{latency:.2f},{reading.flow},{reading.ph},"
                f"{reading.conductivity},{reading.cod},{prediction_real:.2f},{status}\n")
    
    return {
        "prediction_mg_L": round(prediction_real, 2),
        "status": status,
        "latency_ms": round(latency, 2) # Exposing metrics to the user
    }

# --- 7. NEW ENDPOINT: HEALTH CHECK BOARD ---
@app.get("/monitoring/stats")
def get_monitoring_stats():
    """Returns basic drift and performance metrics for the Dashboard."""
    if not os.path.exists(LOG_FILE):
        return {"message": "No data logged yet."}
    
    try:
        df = pd.read_csv(LOG_FILE)
        
        # Calculate recent stats (Last 50 requests)
        recent = df.tail(50)
        
        return {
            "total_requests": len(df),
            "avg_latency_ms": round(recent['latency_ms'].mean(), 2),
            "avg_input_cod": round(recent['cod'].mean(), 2),
            "avg_input_conductivity": round(recent['conductivity'].mean(), 2),
            "drift_status": "Stable" if recent['conductivity'].mean() < 2000 else "DRIFT DETECTED: High Salinity"
        }
    except Exception as e:
        return {"error": str(e)}