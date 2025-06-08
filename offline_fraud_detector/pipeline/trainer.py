from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
from joblib import dump
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import MODEL_PATH

class Trainer:
    """
    Class for training the fraud detection model with hyperparameter tuning.
    """
    def __init__(self):
        self.model = None
        self.best_params = None
        self.feature_importances = None

    def _perform_hyperparameter_tuning(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Args:
            X_train: Training feature matrix
            y_train: Training target vector
            
        Returns:
            Dictionary of best hyperparameters
        """
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        # Create base model
        base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        # Perform grid search
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=3,
            scoring='f1',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        return grid_search.best_params_

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """
        Train the model with hyperparameter tuning and SMOTE.
        
        Args:
            X_train: Training feature matrix
            y_train: Training target vector
        """
        # Handle imbalanced data using SMOTE
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

        # Perform hyperparameter tuning
        print("\nPerforming hyperparameter tuning...")
        self.best_params = self._perform_hyperparameter_tuning(X_resampled, y_resampled)
        print(f"Best parameters found: {self.best_params}")

        # Train model with best parameters
        self.model = RandomForestClassifier(
            **self.best_params,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_resampled, y_resampled)
        
        # Get feature importances
        self.feature_importances = pd.DataFrame({
            'feature': X_resampled.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

    def save_model(self) -> None:
        """
        Save the trained model and feature importances to disk.
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Save model
        dump(self.model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

    def plot_feature_importance(self, n_features: int = 10) -> None:
        """
        Plot the top N most important features.
        
        Args:
            n_features: Number of top features to display
        """
        if self.feature_importances is None:
            raise ValueError("Model not trained yet")

        # Get top N features
        top_features = self.feature_importances.head(n_features)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x='importance',
            y='feature',
            data=top_features,
            palette='viridis'
        )
        plt.title(f'Top {n_features} Most Important Features')
        plt.xlabel('Feature Importance')
        plt.ylabel('Features')
        plt.tight_layout()
        plt.savefig('outputs/feature_importance.png')
        print("Feature importance plot saved to outputs/feature_importance.png")
        plt.close()
