"""
Simplified hypothesis testing script
Run from project root: python scripts/run_hypothesis_tests.py
"""

import pandas as pd
import numpy as np
import sys
import os
from scipy.stats import chi2_contingency, ttest_ind

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_simple_tests():
    """Run simplified hypothesis tests"""
    
    # Load data
    print("Loading data...")
    df = pd.read_csv('data/processed/insurance_data_cleaned.csv', low_memory=False)
    print(f"Loaded {len(df)} records")
    
    # Calculate margin
    df['Margin'] = df['AnnualPremium'] - df['ClaimAmount']
    
    results = []
    
    # Test 1: Province Risk Differences
    print("\n" + "="*60)
    print("TEST 1: Province Risk Differences (Addis Ababa vs Somali)")
    print("="*60)
    
    # Filter for two provinces
    mask = df['Province'].isin(['Addis Ababa', 'Somali'])
    province_df = df[mask]
    
    # Claim frequency test (chi-squared)
    contingency = pd.crosstab(province_df['Province'], province_df['Claimed'])
    chi2, p_freq, dof, expected = chi2_contingency(contingency)
    
    rate_a = contingency.loc['Addis Ababa', True] / contingency.loc['Addis Ababa'].sum() if True in contingency.columns else 0
    rate_b = contingency.loc['Somali', True] / contingency.loc['Somali'].sum() if True in contingency.columns else 0
    
    print(f"Claim Rate - Addis Ababa: {rate_a:.2%}")
    print(f"Claim Rate - Somali: {rate_b:.2%}")
    print(f"Chi-squared p-value: {p_freq:.6f}")
    print(f"Decision: {'REJECT H₀' if p_freq < 0.05 else 'FAIL TO REJECT H₀'}")
    
    results.append({
        'Hypothesis': 'Province Risk Difference',
        'KPI': 'Claim Frequency',
        'Groups': 'Addis Ababa vs Somali',
        'Group A Rate': f"{rate_a:.2%}",
        'Group B Rate': f"{rate_b:.2%}",
        'P-Value': p_freq,
        'Decision': 'Reject H₀' if p_freq < 0.05 else 'Fail to reject H₀'
    })
    
    # Claim severity test (t-test)
    claims_df = df[df['Claimed'] == True]
    severity_a = claims_df[claims_df['Province'] == 'Addis Ababa']['ClaimAmount'].values
    severity_b = claims_df[claims_df['Province'] == 'Somali']['ClaimAmount'].values
    
    if len(severity_a) > 0 and len(severity_b) > 0:
        t_stat, p_sev = ttest_ind(severity_a, severity_b, equal_var=False)
        print(f"\nAvg Severity - Addis Ababa: ${severity_a.mean():,.0f}")
        print(f"Avg Severity - Somali: ${severity_b.mean():,.0f}")
        print(f"t-test p-value: {p_sev:.6f}")
        print(f"Decision: {'REJECT H₀' if p_sev < 0.05 else 'FAIL TO REJECT H₀'}")
        
        results.append({
            'Hypothesis': 'Province Severity Difference',
            'KPI': 'Claim Severity',
            'Groups': 'Addis Ababa vs Somali',
            'Group A Mean': f"${severity_a.mean():,.0f}",
            'Group B Mean': f"${severity_b.mean():,.0f}",
            'P-Value': p_sev,
            'Decision': 'Reject H₀' if p_sev < 0.05 else 'Fail to reject H₀'
        })
    
    # Test 2: Gender Risk Differences
    print("\n" + "="*60)
    print("TEST 2: Gender Risk Differences (Male vs Female)")
    print("="*60)
    
    contingency_gender = pd.crosstab(df['Gender'], df['Claimed'])
    chi2_gender, p_gender_freq, dof, expected = chi2_contingency(contingency_gender)
    
    rate_male = contingency_gender.loc['Male', True] / contingency_gender.loc['Male'].sum() if True in contingency_gender.columns else 0
    rate_female = contingency_gender.loc['Female', True] / contingency_gender.loc['Female'].sum() if True in contingency_gender.columns else 0
    
    print(f"Claim Rate - Male: {rate_male:.2%}")
    print(f"Claim Rate - Female: {rate_female:.2%}")
    print(f"Chi-squared p-value: {p_gender_freq:.6f}")
    print(f"Decision: {'REJECT H₀' if p_gender_freq < 0.05 else 'FAIL TO REJECT H₀'}")
    
    results.append({
        'Hypothesis': 'Gender Risk Difference',
        'KPI': 'Claim Frequency',
        'Groups': 'Male vs Female',
        'Group A Rate': f"{rate_male:.2%}",
        'Group B Rate': f"{rate_female:.2%}",
        'P-Value': p_gender_freq,
        'Decision': 'Reject H₀' if p_gender_freq < 0.05 else 'Fail to reject H₀'
    })
    
    # Test 3: Zip Code Differences
    print("\n" + "="*60)
    print("TEST 3: Zip Code Differences")
    print("="*60)
    
    top_zips = df['ZipCode'].value_counts().head(2).index.tolist()
    print(f"Comparing Zip {top_zips[0]} vs Zip {top_zips[1]}")
    
    mask_zip = df['ZipCode'].isin(top_zips)
    zip_df = df[mask_zip]
    
    contingency_zip = pd.crosstab(zip_df['ZipCode'], zip_df['Claimed'])
    chi2_zip, p_zip_freq, dof, expected = chi2_contingency(contingency_zip)
    
    print(f"Chi-squared p-value: {p_zip_freq:.6f}")
    print(f"Decision: {'REJECT H₀' if p_zip_freq < 0.05 else 'FAIL TO REJECT H₀'}")
    
    results.append({
        'Hypothesis': 'Zip Code Risk Difference',
        'KPI': 'Claim Frequency',
        'Groups': f'{top_zips[0]} vs {top_zips[1]}',
        'P-Value': p_zip_freq,
        'Decision': 'Reject H₀' if p_zip_freq < 0.05 else 'Fail to reject H₀'
    })
    
    # Margin test for zip codes
    margin_a = zip_df[zip_df['ZipCode'] == top_zips[0]]['Margin'].values
    margin_b = zip_df[zip_df['ZipCode'] == top_zips[1]]['Margin'].values
    
    if len(margin_a) > 0 and len(margin_b) > 0:
        t_stat, p_margin = ttest_ind(margin_a, margin_b, equal_var=False)
        print(f"\nAvg Margin - Zip {top_zips[0]}: ${margin_a.mean():,.0f}")
        print(f"Avg Margin - Zip {top_zips[1]}: ${margin_b.mean():,.0f}")
        print(f"t-test p-value: {p_margin:.6f}")
        print(f"Decision: {'REJECT H₀' if p_margin < 0.05 else 'FAIL TO REJECT H₀'}")
        
        results.append({
            'Hypothesis': 'Zip Code Margin Difference',
            'KPI': 'Margin',
            'Groups': f'{top_zips[0]} vs {top_zips[1]}',
            'Group A Mean': f"${margin_a.mean():,.0f}",
            'Group B Mean': f"${margin_b.mean():,.0f}",
            'P-Value': p_margin,
            'Decision': 'Reject H₀' if p_margin < 0.05 else 'Fail to reject H₀'
        })
    
    # Save results
    results_df = pd.DataFrame(results)
    os.makedirs('reports', exist_ok=True)
    results_df.to_csv('reports/hypothesis_test_results.csv', index=False)
    
    print("\n" + "="*60)
    print("SUMMARY TABLE")
    print("="*60)
    print(results_df.to_string(index=False))
    
    return results_df

if __name__ == "__main__":
    run_simple_tests()