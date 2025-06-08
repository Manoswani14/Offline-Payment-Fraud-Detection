import pandas as pd
from joblib import load
from typing import Union
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from config import MODEL_PATH, PREDICTION_OUTPUT

class Predictor:
    """
    Class for making predictions on new transaction data.
    """
    def __init__(self):
        self.model = None

    def load_model(self) -> None:
        """
        Load the trained model from disk.
        """
        try:
            self.model = load(MODEL_PATH)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")

    def predict(self, input_file: Union[str, Path], output_file: Union[str, Path] = PREDICTION_OUTPUT) -> None:
        """
        Make predictions on new transaction data and save results.
        
        Args:
            input_file: Path to the input CSV file containing new transactions
            output_file: Path where predictions will be saved
        """
        # Load the model
        self.load_model()
        
        # Load and preprocess new data
        df = pd.read_csv(input_file)
        
        # Ensure feature order matches training data
        required_features = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
        
        # Check if all required features are present
        missing_features = [feat for feat in required_features if feat not in df.columns]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Reorder columns to match training data
        df = df[required_features]
        
        # Scale features
        scaler = StandardScaler()
        for feature in ['Amount', 'Time']:
            df[feature] = scaler.fit_transform(df[[feature]])
        
        # Make predictions
        predictions = self.model.predict(df)
        
        # Add predictions to original dataframe
        df['Prediction'] = predictions
        
        # Save results
        df.to_csv(output_file, index=False)
        print(f"Predictions saved to {output_file}")
