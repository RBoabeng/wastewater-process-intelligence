import pandas as pd
import numpy as np
from typing import Tuple

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads the wastewater dataset from a CSV file.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame: Raw dataframe indexed by Date.
    
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {filepath} was not found.")

def clean_data(df: pd.DataFrame, remove_outliers: bool = True) -> pd.DataFrame:
    """
    Cleans the raw dataframe by removing errors and handling missing values.

    This function addresses the '99% Rule' discovered during EDA, removing 
    extreme COD outliers that represent sensor malfunctions.

    Args:
        df (pd.DataFrame): The raw input dataframe.
        remove_outliers (bool): If True, caps COD at the 99th percentile.

    Returns:
        pd.DataFrame: Cleaned dataframe ready for feature engineering.
    """
    df_clean = df.copy()
    
    if remove_outliers:
        cap = df_clean['DQO_E_Input_COD'].quantile(0.99)
        df_clean = df_clean[df_clean['DQO_E_Input_COD'] < cap]
    
    return df_clean