from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from typing import Tuple
import numpy as np
import pandas as pd

class Evaluator:
    """
    Class for evaluating the performance of the fraud detection model.
    """
    def evaluate(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """
        Evaluate the model performance and return metrics.
        
        Args:
            model: Trained model
            X_test: Test feature matrix
            y_test: Test target vector
            
        Returns:
            dict: Dictionary containing evaluation metrics
        """
        # Get predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Print detailed report
        print("\nModel Evaluation Report:")
        print("-" * 50)
        print("Confusion Matrix:")
        print(np.array(metrics['confusion_matrix']))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return metrics
