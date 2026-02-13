import os
import yaml
from data_loader import load_data, clean_data
from features import add_seasonality, select_features
from model import train_model, save_model

# --- ROBUST PATH SETUP ---
# 1. Get the folder where THIS script (main.py) lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Get the Project Root (one level up from src)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_config(config_name="config.yaml"):
    """Loads config.yaml from the Project Root."""
    config_path = os.path.join(PROJECT_ROOT, config_name)
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def run_pipeline():
    # Load Config
    config = load_config()
    
    # Construct Absolute Paths using the Project Root
    # This prevents "File Not Found" errors forever
    raw_data_path = os.path.join(PROJECT_ROOT, config['paths']['raw_data'])
    model_save_path = os.path.join(PROJECT_ROOT, config['paths']['model_save'])
    
    # Ensure models directory exists
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    
    print(f"Loading Data from: {raw_data_path}")
    
    # ... (Rest of the code stays exactly the same) ...
    df = load_data(raw_data_path)
    df = clean_data(df)
    
    print("Engineering Features...")
    df = add_seasonality(df)
    
    X = select_features(df)
    y = df['DBO_E_Input_BOD']
    
    model, metrics = train_model(X, y, config)
    
    save_model(model, model_save_path)
    print("Pipeline Finished Successfully.")

if __name__ == "__main__":
    run_pipeline()