from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Tuple
import pandas as pd
from config import TEST_SIZE, SCALING_FEATURES

class Preprocessor:
    """
    Class for preprocessing the transaction data.
    """
    def __init__(self):
        self.scaler = StandardScaler()

    def fit_transform(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Preprocess the data by scaling selected features and splitting into features and labels.
        
        Args:
            df: Input DataFrame containing transaction data
            
        Returns:
            Tuple containing (X, y) where X is the feature matrix and y is the target vector
        """
        # Scale selected features
        for feature in SCALING_FEATURES:
            df[feature] = self.scaler.fit_transform(df[[feature]])

        # Split into features and target
        X = df.drop('Class', axis=1)
        y = df['Class']
        
        return X, y

    def split_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple:
        """
        Split the data into training and testing sets.
        
        Args:
            X: Feature matrix
            y: Target vector
            
        Returns:
            Tuple containing (X_train, X_test, y_train, y_test)
        """
        return train_test_split(X, y, test_size=TEST_SIZE, random_state=42, stratify=y)
