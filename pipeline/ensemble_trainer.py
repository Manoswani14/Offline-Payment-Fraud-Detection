from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
from sklearn.base import BaseEstimator, ClassifierMixin
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import numpy as np
import joblib
import os
from utils.logger import Logger

class EnsembleTrainer(BaseEstimator, ClassifierMixin):
    def __init__(self, n_estimators=100, random_state=42):
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.models = []
        self.logger = Logger('ensemble_trainer').get_logger()
        
    def create_base_models(self):
        """Create base models for the ensemble"""
        return [
            ('rf', RandomForestClassifier(
                n_estimators=self.n_estimators,
                random_state=self.random_state,
                class_weight='balanced'
            )),
            ('gb', GradientBoostingClassifier(
                n_estimators=self.n_estimators,
                random_state=self.random_state
            )),
            ('lr', LogisticRegression(
                class_weight='balanced',
                random_state=self.random_state,
                max_iter=1000
            ))
        ]
    
    def fit(self, X, y):
        """Train the ensemble model"""
        self.logger.info("Starting ensemble training...")
        
        # Create SMOTE pipeline for each model
        for name, model in self.create_base_models():
            pipeline = Pipeline([
                ('smote', SMOTE(random_state=self.random_state)),
                ('model', model)
            ])
            
            # Perform cross-validation
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
            scores = cross_val_score(
                pipeline, X, y,
                cv=cv,
                scoring='roc_auc',
                n_jobs=-1
            )
            
            # Log cross-validation results
            self.logger.info(f"{name} CV scores: {scores}")
            self.logger.info(f"{name} Mean CV score: {scores.mean():.4f}")
            
            # Train on full dataset
            pipeline.fit(X, y)
            self.models.append((name, pipeline))
            
        self.logger.info("Ensemble training completed")
        return self
    
    def predict_proba(self, X):
        """Get probability predictions from all models"""
        probas = []
        for _, model in self.models:
            probas.append(model.predict_proba(X)[:, 1])
        return np.mean(probas, axis=0)
    
    def predict(self, X, threshold=0.5):
        """Get final predictions"""
        probas = self.predict_proba(X)
        return (probas >= threshold).astype(int)
    
    def evaluate(self, X, y):
        """Evaluate the ensemble model"""
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)
        
        metrics = {
            'roc_auc': roc_auc_score(y, y_proba),
            'precision': precision_score(y, y_pred),
            'recall': recall_score(y, y_pred),
            'f1': f1_score(y, y_pred)
        }
        
        self.logger.info("Ensemble evaluation metrics:")
        for metric, value in metrics.items():
            self.logger.info(f"{metric}: {value:.4f}")
        
        return metrics
    
    def save(self, path='models/ensemble_model.pkl'):
        """Save the ensemble model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
        self.logger.info(f"Model saved to {path}")
    
    @classmethod
    def load(cls, path='models/ensemble_model.pkl'):
        """Load the ensemble model"""
        return joblib.load(path)
