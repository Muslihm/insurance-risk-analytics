import pandas as pd
import numpy as np

def create_second_version(input_path, output_path):
    """Create enhanced second version with additional features"""
    
    df = pd.read_csv(input_path)
    
    # Add additional derived features
    df['PremiumPerRisk'] = df['AnnualPremium'] / df['RiskScore'].clip(lower=1)
    
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 25, 35, 50, 65, 100], 
                             labels=['18-25', '26-35', '36-50', '51-65', '65+'])
    
    df['NCDCategory'] = pd.cut(df['NCD'], bins=[-1, 0, 20, 40, 60, 100],
                                labels=['None', 'Low', 'Medium', 'High', 'Max'])
    
    df['ClaimSeverity'] = np.where(df['ClaimAmount'] == 0, 'No Claim',
                            np.where(df['ClaimAmount'] < 5000, 'Minor',
                            np.where(df['ClaimAmount'] < 15000, 'Moderate', 'Severe')))
    
    # Add flag for high-risk customers
    df['IsHighRisk'] = (df['RiskScore'] > 70) & (df['PastClaims'] > 2)
    
    df.to_csv(output_path, index=False)
    print(f"Second version saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"New features: PremiumPerRisk, AgeGroup, NCDCategory, ClaimSeverity, IsHighRisk")

if __name__ == "__main__":
    create_second_version('data/processed/insurance_data_cleaned.csv', 
                         'data/processed/insurance_data_enhanced.csv')