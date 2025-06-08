import pandas as pd
from typing import Union
from pathlib import Path
from config import DATA_DIR

def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load and validate the dataset.
    
    Args:
        file_path: Path to the CSV file containing transaction data
        
    Returns:
        pd.DataFrame: Loaded and validated dataset
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If required columns are missing
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found at {file_path}")

    # Validate required columns
    required_columns = ['Time', 'Amount', 'Class']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return df
