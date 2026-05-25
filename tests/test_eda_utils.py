import pytest
import numpy as np

class EDAAnalyzer:
    """Exploratory Data Analysis utilities for insurance data"""
    
    def __init__(self, df):
        """Initialize with DataFrame"""
        self.df = df
    
    def calculate_loss_ratio(self):
        """Calculate loss ratio (claims/premiums)"""
        # Assuming you have columns like 'TotalClaims' and 'TotalPremium'
        # Adjust column names based on your actual data
        total_claims = self.df['TotalClaims'].sum() if 'TotalClaims' in self.df.columns else 0
        total_premium = self.df['TotalPremium'].sum() if 'TotalPremium' in self.df.columns else 1
        
        if total_premium == 0:
            return 0
        
        loss_ratio = total_claims / total_premium
        return min(max(loss_ratio, 0), 1)  # Clamp between 0 and 1
    
    def detect_outliers(self, column):
        """Detect outliers in a column using IQR method"""
        if column not in self.df.columns:
            return [], 0
        
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        return outliers, len(outliers)