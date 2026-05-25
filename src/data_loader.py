"""Data loading utilities for insurance claims data"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


class InsuranceDataLoader:
    """Load and validate insurance claims dataset"""
    
    def __init__(self, data_path: str = "data/insurance_claims.csv"):
        self.data_path = Path(data_path)
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """Load CSV data with proper type handling"""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.data = pd.read_csv(self.data_path)
        return self.data
    
    def validate_data(self) -> Tuple[bool, dict]:
        """Validate data integrity and return quality report"""
        if self.data is None:
            return False, {"error": "Data not loaded"}
        
        report = {
            "row_count": len(self.data),
            "column_count": len(self.data.columns),
            "missing_values": self.data.isnull().sum().to_dict(),
            "duplicate_rows": self.data.duplicated().sum(),
        }
        
        return True, report


def create_sample_data() -> pd.DataFrame:
    """Generate sample data for testing"""
    np.random.seed(42)
    n_samples = 1000
    
    provinces = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Mpumalanga']
    genders = ['Male', 'Female']
    vehicle_types = ['Sedan', 'SUV', 'Hatchback', 'Pickup', 'Coupe']
    cover_types = ['Comprehensive', 'Third Party', 'Third Party Fire and Theft']
    vehicle_makes = ['Toyota', 'Volkswagen', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Nissan', 'Hyundai']
    
    data = {
        'PolicyID': range(1, n_samples + 1),
        'Province': np.random.choice(provinces, n_samples),
        'Gender': np.random.choice(genders, n_samples),
        'VehicleType': np.random.choice(vehicle_types, n_samples),
        'VehicleMake': np.random.choice(vehicle_makes, n_samples),
        'CoverType': np.random.choice(cover_types, n_samples),
        'TotalPremium': np.random.uniform(2000, 8000, n_samples),
        'TotalClaims': np.random.exponential(500, n_samples),
        'CustomValueEstimate': np.random.uniform(50000, 500000, n_samples),
        'Age': np.random.uniform(18, 70, n_samples),
        'VehicleAge': np.random.uniform(0, 20, n_samples),
        'NumberOfClaims': np.random.poisson(0.1, n_samples),
    }
    
    return pd.DataFrame(data)