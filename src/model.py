import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from typing import Tuple, Dict

def train_model(X: pd.DataFrame, y: pd.Series, config: Dict) -> Tuple[Pipeline, Dict[str, float]]:
    """
    Trains a model based on the configuration 'type' (RandomForest or SVM).
    """
    # 1. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Log Transform Target
    y_train_log = np.log1p(y_train)
    y_test_log = np.log1p(y_test)

    # 3. Select Algorithm from Config
    model_type = config['model']['type']
    
    if model_type == "RandomForest":
        params = config['model']['random_forest']
        # Pipeline isn't strictly needed for RF, but good for consistency
        model = Pipeline([
            ('scaler', StandardScaler()), 
            ('regressor', RandomForestRegressor(**params))
        ])
    elif model_type == "SVM":
        params = config['model']['svm']
        model = Pipeline([
            ('scaler', StandardScaler()), 
            ('regressor', SVR(**params))
        ])
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # 4. MLflow Logging
    mlflow.set_experiment("Wastewater_Production_Pipeline")
    
    with mlflow.start_run(run_name=f"Train_{model_type}"):
        mlflow.log_params(params)
        mlflow.log_param("model_type", model_type)
        
        print(f"Training {model_type}...")
        model.fit(X_train, y_train_log)
        
        # 5. Evaluate
        y_pred_log = model.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        y_true = np.expm1(y_test_log)
        
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        metrics = {"rmse": rmse, "r2": r2}
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Training Complete. RMSE: {rmse:.2f} mg/L | R2: {r2:.3f}")
        return model, metrics

def save_model(model, filepath: str):
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")