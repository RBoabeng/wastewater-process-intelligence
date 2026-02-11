import pandas as pd
import numpy as np
import os

def load_uci_data(filepath='data/raw/water-treatment.data'):
    """
    Loads and cleans the UCI Wastewater Treatment Plant dataset.
    
    Args:
        filepath (str): Path to the raw .data file.
        
    Returns:
        pd.DataFrame: Cleaned dataframe with professional column names.
    """
    
    # 1. Define the "Professional" Engineering Column Names
    column_names = [
        "Date",
        "Q_E_Input_Flow", "ZN_E_Input_Zinc", "PH_E_Input_pH", "DBO_E_Input_BOD", "DQO_E_Input_COD", "SS_E_Input_SS", "SSV_E_Input_Volatile_SS", "SED_E_Input_Sediment", "COND_E_Input_Conductivity",
        "PH_P_Primary_pH", "DBO_P_Primary_BOD", "SS_P_Primary_SS", "SSV_P_Primary_Volatile_SS", "SED_P_Primary_Sediment", "COND_P_Primary_Conductivity",
        "PH_D_Secondary_pH", "DBO_D_Secondary_BOD", "DQO_D_Secondary_COD", "SS_D_Secondary_SS", "SSV_D_Secondary_Volatile_SS", "SED_D_Secondary_Sediment", "COND_D_Secondary_Conductivity",
        "PH_S_Output_pH", "DBO_S_Output_BOD", "DQO_S_Output_COD", "SS_S_Output_SS", "SSV_S_Output_Volatile_SS", "SED_S_Output_Sediment", "COND_S_Output_Conductivity",
        "RD_DBO_P_Performance_Input_Primary_BOD", "RD_SS_P_Performance_Input_Primary_SS", "RD_SED_P_Performance_Input_Primary_Sediment",
        "RD_DBO_S_Performance_Input_Secondary_BOD", "RD_DQO_S_Performance_Input_Secondary_COD", "RD_DBO_G_Performance_Global_BOD", "RD_DQO_G_Performance_Global_COD", "RD_SS_G_Performance_Global_SS", "RD_SED_G_Performance_Global_Sediment"
    ]

    # 2. Load Data
    try:
        df = pd.read_csv(filepath, header=None, na_values='?', names=column_names)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    # 3. FIX: Handle the 'D-' prefix in dates
    # We replace 'D-' with nothing, so 'D-1/3/90' becomes '1/3/90'
    try:
        df['Date'] = df['Date'].astype(str).str.replace('D-', '', regex=False)
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    except Exception as e:
        print(f"Date parsing warning: {e}")

    # 4. FIX: Modern Imputation Strategy
    # Replaced deprecated fillna(method='ffill') with ffill()
    original_missing = df.isna().sum().sum()
    
    df.ffill(inplace=True) # Forward fill (propagate last valid observation)
    df.bfill(inplace=True) # Backward fill (catch any missing at the start)
    
    print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
    print(f"Imputed {original_missing} missing values using Forward Fill.")

    return df

if __name__ == "__main__":
    df = load_uci_data()
    if df is not None:
        print("\nFirst 5 rows of the clean engineering data:")
        print(df.head())
        
        output_path = 'data/processed/clean_wastewater_data.csv'
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nSaved processed data to {output_path}")