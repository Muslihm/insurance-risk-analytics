import pytest
import pandas as pd
from src.data_loader import InsuranceDataLoader, create_sample_data

def test_create_sample_data():
df = create_sample_data()
assert len(df) == 1000
assert 'TotalPremium' in df.columns
assert 'TotalClaims' in df.columns

def test_insurance_data_loader():
loader = InsuranceDataLoader()
assert loader.data_path.name == 'insurance_claims.csv'
