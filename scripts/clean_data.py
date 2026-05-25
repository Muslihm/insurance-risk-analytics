import pandas as pd
import numpy as np

def load_raw_data(filepath):
    """Load raw insurance data"""
    return pd.read_csv(filepath)

def clean_insurance_data(df):
    """Clean and transform insurance data"""
    
    # Create a copy to avoid warnings
    df_clean = df.copy()
    
    # Convert TransactionDate to datetime
    df_clean['TransactionDate'] = pd.to_datetime(df_clean['TransactionDate'])
    
    # Extract date features
    df_clean['TransactionYear'] = df_clean['TransactionDate'].dt.year
    df_clean['TransactionMonth'] = df_clean['TransactionDate'].dt.month
    
    # Handle missing values (if any)
    df_clean = df_clean.dropna()
    
    # Create derived features
    df_clean['ClaimRatio'] = df_clean['ClaimAmount'] / df_clean['AnnualPremium'].clip(lower=1)
    df_clean['ClaimRatio'] = df_clean['ClaimRatio'].fillna(0)
    
    # Create risk categories
    df_clean['RiskCategory'] = pd.cut(
        df_clean['RiskScore'],
        bins=[0, 30, 50, 70, 100],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create income groups
    df_clean['IncomeGroup'] = pd.cut(
        df_clean['AnnualIncome'],
        bins=[0, 50000, 100000, 200000, float('inf')],
        labels=['Low', 'Medium-Low', 'Medium-High', 'High']
    )
    
    # Convert boolean columns
    df_clean['Claimed'] = df_clean['Claimed'].astype(bool)
    
    return df_clean

def main():
    """Main execution function"""
    
    # Load raw data - UPDATED PATH
    print("Loading raw data... - clean_data.py:51")
    raw_df = load_raw_data('data/raw/insurance_data.csv')
    print(f"Raw data shape: {raw_df.shape} - clean_data.py:53")
    
    # Clean data
    print("Cleaning data... - clean_data.py:56")
    cleaned_df = clean_insurance_data(raw_df)
    print(f"Cleaned data shape: {cleaned_df.shape} - clean_data.py:58")
    
    # Save cleaned data
    cleaned_df.to_csv('data/processed/insurance_data_cleaned.csv', index=False)
    print("Cleaned data saved to data/processed/insurance_data_cleaned.csv - clean_data.py:62")
    
    # Generate summary statistics
    summary = cleaned_df.describe()
    summary.to_csv('data/processed/data_summary.csv')
    print("Summary statistics saved - clean_data.py:67")
    
    return cleaned_df

if __name__ == "__main__":
    df = main()