import pandas as pd
import numpy as np
from pathlib import Path

class InsuranceDataLoader:
    def __init__(self, data_path=None):
        """Initialize the data loader with a path to the data file"""
        if data_path is None:
            # Use the actual data file you have
            self.data_path = Path(__file__).parent.parent / 'insurance_data.csv'
        else:
            self.data_path = Path(data_path)
        
        self.data = None
    
    def load_data(self):
        """Load the insurance claims data from CSV file"""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.data = pd.read_csv(self.data_path)
        return self.data
    
    def get_summary(self):
        """Get summary statistics of the data"""
        if self.data is None:
            return None
        return self.data.describe()
    
    def get_shape(self):
        """Get the shape of the data"""
        if self.data is None:
            return (0, 0)
        return self.data.shape
    
    def get_columns(self):
        """Get column names"""
        if self.data is None:
            return []
        return list(self.data.columns)

def create_sample_data(n_samples=100):
    """Create sample insurance data for testing"""
    np.random.seed(42)
    
    data = {
        'TotalPremium': np.random.uniform(500, 5000, n_samples),
        'TotalClaims': np.random.uniform(0, 3000, n_samples),
        'Age': np.random.randint(18, 80, n_samples),
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'VehicleType': np.random.choice(['Sedan', 'SUV', 'Hatchback'], n_samples),
        'Province': np.random.choice(['Addis Ababa', 'Oromia', 'Amhara', 'Tigray', 'Somali'], n_samples),
    }
    
    # Add some correlation - higher premiums tend to have higher claims
    data['TotalClaims'] = data['TotalClaims'] * (data['TotalPremium'] / data['TotalPremium'].mean()) * 0.5
    
    df = pd.DataFrame(data)
    
    # Ensure loss ratio is between 0 and 1
    df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']
    df['LossRatio'] = df['LossRatio'].clip(0, 1)
    
    return df