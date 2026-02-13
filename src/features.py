import pandas as pd
import numpy as np

def add_seasonality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds cyclical time features to handle biological seasonality.

    Based on EDA, BOD loads vary significantly between Winter (Dec) and 
    Summer (Aug). This function adds Sine and Cosine transformations 
    of the month.

    Args:
        df (pd.DataFrame): The cleaned dataframe.

    Returns:
        pd.DataFrame: Dataframe with 'sin_month' and 'cos_month' columns added.
    """
    df = df.copy()
    df['Month'] = df.index.month
    df['sin_month'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['cos_month'] = np.cos(2 * np.pi * df['Month'] / 12)
    df.drop(columns=['Month'], inplace=True)
    return df

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selects the specific orthogonal sensors required for the model.

    Includes:
    - Flow (Q_E): Volume
    - pH (PH_E): Acidity
    - Conductivity (COND_E): Dissolved Solids (The 'Rain Detector')
    - COD (DQO_E): Chemical Oxygen Demand (The 'BOD Proxy')

    Args:
        df (pd.DataFrame): The dataframe with all sensors.

    Returns:
        pd.DataFrame: A subset dataframe with only the model features.
    """
    features = [
        'Q_E_Input_Flow', 
        'PH_E_Input_pH', 
        'COND_E_Input_Conductivity', 
        'DQO_E_Input_COD', 
        'sin_month', 
        'cos_month'
    ]
    return df[features]