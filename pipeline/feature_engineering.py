import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Keep 95% variance
        self.selector = SelectKBest(f_classif, k=20)  # Select top 20 features
        self.selected_features = None
    
    def create_time_features(self, df):
        """Create time-based features"""
        df['Hour'] = df['Time'] % 24
        df['DayOfWeek'] = (df['Time'] // (24 * 3600)) % 7
        df['Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
        return df
    
    def create_amount_features(self, df):
        """Create amount-based features"""
        df['LogAmount'] = np.log(df['Amount'] + 1)
        df['SqrtAmount'] = np.sqrt(df['Amount'])
        return df
    
    def create_transaction_patterns(self, df):
        """Create transaction pattern features"""
        df['TransactionRate'] = df['Amount'] / df['Time']
        df['TransactionRate'] = df['TransactionRate'].fillna(0)
        return df
    
    def transform(self, df):
        """Apply all feature transformations"""
        # Create new features
        df = self.create_time_features(df)
        df = self.create_amount_features(df)
        df = self.create_transaction_patterns(df)
        
        # Scale features
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        
        # Apply PCA
        pca_features = self.pca.fit_transform(df[numeric_cols])
        df_pca = pd.DataFrame(pca_features, columns=[f'PC_{i}' for i in range(pca_features.shape[1])])
        
        # Select best features
        X = df_pca
        y = df['Class'] if 'Class' in df.columns else None
        
        if y is not None:
            self.selector.fit(X, y)
            self.selected_features = X.columns[self.selector.get_support()]
            X = X[self.selected_features]
        else:
            X = X[self.selected_features]
        
        return X
