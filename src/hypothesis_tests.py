"""
Hypothesis Testing Module for Insurance Risk Analytics

This module provides statistical testing functions for:
- Claim Frequency (categorical KPI) - uses chi-squared test
- Claim Severity (numerical KPI) - uses t-test/z-test
- Margin (numerical KPI) - uses t-test

Author: Data Science Team
Date: 2026-05-25
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind, f_oneway
from statsmodels.stats.proportion import proportions_ztest
import warnings
warnings.filterwarnings('ignore')


class HypothesisTester:
    """
    A class for performing hypothesis tests on insurance data.
    
    Attributes:
        df (pd.DataFrame): The insurance dataset
        alpha (float): Significance level (default 0.05)
    """
    
    def __init__(self, df, alpha=0.05):
        """
        Initialize the HypothesisTester with data.
        
        Args:
            df: DataFrame containing insurance data
            alpha: Significance level for hypothesis testing
        """
        self.df = df
        self.alpha = alpha
        self.results = []
    
    def prepare_claim_frequency(self, group_col, group_a, group_b):
        """
        Prepare contingency table for claim frequency test.
        
        Args:
            group_col: Column name for grouping (e.g., 'Province')
            group_a: Value for Group A (baseline/control)
            group_b: Value for Group B (test)
            
        Returns:
            contingency_table: 2x2 table for chi-squared test
        """
        # Filter data for the two groups
        mask = self.df[group_col].isin([group_a, group_b])
        filtered_df = self.df[mask].copy()
        
        # Create contingency table
        # Rows: Group A vs Group B
        # Columns: Claimed (True/False)
        contingency_table = pd.crosstab(
            filtered_df[group_col], 
            filtered_df['Claimed'],
            margins=False
        )
        
        # Ensure we have both groups and both outcomes
        if len(contingency_table) != 2:
            raise ValueError(f"Expected 2 groups, got {len(contingency_table)}")
        
        # Reorder rows to match Group A, Group B
        contingency_table = contingency_table.reindex([group_a, group_b])
        
        return contingency_table
    
    def test_claim_frequency(self, group_col, group_a, group_b, hypothesis_name):
        """
        Test if claim frequency differs between two groups.
        
        Uses Chi-squared test for independence.
        
        Args:
            group_col: Column name for grouping
            group_a: Control group value
            group_b: Test group value
            hypothesis_name: Description of the hypothesis
            
        Returns:
            dict: Test results including p-value, decision, statistics
        """
        # Prepare contingency table
        contingency_table = self.prepare_claim_frequency(group_col, group_a, group_b)
        
        # Calculate proportions
        n_a = contingency_table.loc[group_a].sum()
        n_b = contingency_table.loc[group_b].sum()
        claims_a = contingency_table.loc[group_a, True] if True in contingency_table.columns else 0
        claims_b = contingency_table.loc[group_b, True] if True in contingency_table.columns else 0
        rate_a = claims_a / n_a if n_a > 0 else 0
        rate_b = claims_b / n_b if n_b > 0 else 0
        
        # Perform chi-squared test
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        
        # Decision
        decision = "Reject H₀" if p_value < self.alpha else "Fail to reject H₀"
        
        # Effect size (risk difference)
        risk_difference = rate_b - rate_a
        relative_risk = rate_b / rate_a if rate_a > 0 else np.inf
        
        result = {
            'hypothesis': hypothesis_name,
            'kpi': 'Claim Frequency',
            'group_a': group_a,
            'group_b': group_b,
            'n_a': n_a,
            'n_b': n_b,
            'rate_a': f"{rate_a:.2%}",
            'rate_b': f"{rate_b:.2%}",
            'test': 'Chi-squared',
            'chi2': chi2,
            'p_value': p_value,
            'decision': decision,
            'risk_difference': f"{risk_difference:.2%}",
            'relative_risk': f"{relative_risk:.2f}",
            'significant': p_value < self.alpha
        }
        
        self.results.append(result)
        return result
    
    def prepare_severity_data(self, group_col, group_a, group_b):
        """
        Prepare data for claim severity test.
        
        Args:
            group_col: Column name for grouping
            group_a: Value for Group A
            group_b: Value for Group B
            
        Returns:
            severity_a, severity_b: Arrays of claim amounts for each group
        """
        # Filter to only claims
        claims_df = self.df[self.df['Claimed'] == True].copy()
        
        # Filter for the two groups
        severity_a = claims_df[claims_df[group_col] == group_a]['ClaimAmount'].values
        severity_b = claims_df[claims_df[group_col] == group_b]['ClaimAmount'].values
        
        if len(severity_a) == 0 or len(severity_b) == 0:
            raise ValueError(f"Insufficient claims data for {group_a} or {group_b}")
        
        return severity_a, severity_b
    
    def test_claim_severity(self, group_col, group_a, group_b, hypothesis_name):
        """
        Test if claim severity differs between two groups.
        
        Uses two-sample t-test (or Welch's t-test for unequal variances).
        
        Args:
            group_col: Column name for grouping
            group_a: Control group value
            group_b: Test group value
            hypothesis_name: Description of the hypothesis
            
        Returns:
            dict: Test results including p-value, decision, statistics
        """
        severity_a, severity_b = self.prepare_severity_data(group_col, group_a, group_b)
        
        # Calculate means
        mean_a = severity_a.mean()
        mean_b = severity_b.mean()
        
        # Perform t-test (Welch's t-test assumes unequal variances)
        t_stat, p_value = ttest_ind(severity_a, severity_b, equal_var=False)
        
        # Decision
        decision = "Reject H₀" if p_value < self.alpha else "Fail to reject H₀"
        
        # Effect size (Cohen's d approximation)
        pooled_std = np.sqrt((np.var(severity_a) + np.var(severity_b)) / 2)
        cohens_d = (mean_b - mean_a) / pooled_std if pooled_std > 0 else 0
        
        result = {
            'hypothesis': hypothesis_name,
            'kpi': 'Claim Severity',
            'group_a': group_a,
            'group_b': group_b,
            'n_a': len(severity_a),
            'n_b': len(severity_b),
            'mean_a': f"${mean_a:,.0f}",
            'mean_b': f"${mean_b:,.0f}",
            'test': "Welch's t-test",
            't_stat': t_stat,
            'p_value': p_value,
            'decision': decision,
            'cohens_d': f"{cohens_d:.2f}",
            'significant': p_value < self.alpha
        }
        
        self.results.append(result)
        return result
    
    def test_margin(self, group_col, group_a, group_b, hypothesis_name):
        """
        Test if margin (profit) differs between two groups.
        
        Margin = TotalPremium - TotalClaims
        
        Args:
            group_col: Column name for grouping
            group_a: Control group value
            group_b: Test group value
            hypothesis_name: Description of the hypothesis
            
        Returns:
            dict: Test results including p-value, decision, statistics
        """
        # Calculate margin per policy
        df_copy = self.df.copy()
        df_copy['Margin'] = df_copy['AnnualPremium'] - df_copy['ClaimAmount']
        
        # Filter for the two groups
        margin_a = df_copy[df_copy[group_col] == group_a]['Margin'].values
        margin_b = df_copy[df_copy[group_col] == group_b]['Margin'].values
        
        # Calculate means
        mean_a = margin_a.mean()
        mean_b = margin_b.mean()
        
        # Perform t-test
        t_stat, p_value = ttest_ind(margin_a, margin_b, equal_var=False)
        
        # Decision
        decision = "Reject H₀" if p_value < self.alpha else "Fail to reject H₀"
        
        result = {
            'hypothesis': hypothesis_name,
            'kpi': 'Margin (Premium - Claims)',
            'group_a': group_a,
            'group_b': group_b,
            'n_a': len(margin_a),
            'n_b': len(margin_b),
            'mean_a': f"${mean_a:,.0f}",
            'mean_b': f"${mean_b:,.0f}",
            'test': "Welch's t-test",
            't_stat': t_stat,
            'p_value': p_value,
            'decision': decision,
            'significant': p_value < self.alpha
        }
        
        self.results.append(result)
        return result
    
    def get_results_table(self):
        """
        Return a formatted DataFrame of all test results.
        
        Returns:
            pd.DataFrame: Summary of all hypothesis tests
        """
        results_df = pd.DataFrame(self.results)
        
        # Format p-values
        results_df['p_value_formatted'] = results_df['p_value'].apply(
            lambda x: f"{x:.4f}" if x >= 0.0001 else f"{x:.2e}"
        )
        
        return results_df
    
    def print_summary(self):
        """
        Print a formatted summary of all hypothesis tests.
        """
        print("\n - hypothesis_tests.py:281" + "="*80)
        print("HYPOTHESIS TESTING SUMMARY - hypothesis_tests.py:282")
        print("= - hypothesis_tests.py:283"*80)
        print(f"Significance Level (α): {self.alpha} - hypothesis_tests.py:284")
        print(f"Decision Rule: Reject H₀ if p < {self.alpha} - hypothesis_tests.py:285")
        print(""*80)
        
        for i, result in enumerate(self.results, 1):
            print(f"\n{i}. {result['hypothesis']} - hypothesis_tests.py:289")
            print(f"KPI: {result['kpi']} - hypothesis_tests.py:290")
            print(f"Groups: {result['group_a']} (n={result['n_a']}) vs {result['group_b']} (n={result['n_b']}) - hypothesis_tests.py:291")
            print(f"Test: {result['test']} - hypothesis_tests.py:292")
            print(f"pvalue: {result['p_value']:.6f} - hypothesis_tests.py:293")
            print(f"Decision: {result['decision']} - hypothesis_tests.py:294")
            
            if result['kpi'] == 'Claim Frequency':
                print(f"Rate: {result['group_a']}={result['rate_a']}, {result['group_b']}={result['rate_b']} - hypothesis_tests.py:297")
                print(f"Risk Difference: {result['risk_difference']} - hypothesis_tests.py:298")
            elif result['kpi'] == 'Claim Severity':
                print(f"Mean: {result['group_a']}={result['mean_a']}, {result['group_b']}={result['mean_b']} - hypothesis_tests.py:300")
                print(f"Cohen's d: {result['cohens_d']} - hypothesis_tests.py:301")
            else:
                print(f"Mean Margin: {result['group_a']}={result['mean_a']}, {result['group_b']}={result['mean_b']} - hypothesis_tests.py:303")
            
            if result['significant']:
                print(f"✅ REJECT H₀: Significant difference detected - hypothesis_tests.py:306")
            else:
                print(f"❌ FAIL TO REJECT H₀: No significant difference detected - hypothesis_tests.py:308")
        
        print("\n - hypothesis_tests.py:310" + "="*80)
        print("END OF SUMMARY - hypothesis_tests.py:311")
        print("= - hypothesis_tests.py:312"*80)


def run_all_hypothesis_tests(df):
    """
    Run all predefined hypothesis tests.
    
    Args:
        df: DataFrame containing insurance data
        
    Returns:
        HypothesisTester: Tester object with results
    """
    tester = HypothesisTester(df, alpha=0.05)
    
    print("= - hypothesis_tests.py:327"*80)
    print("RUNNING HYPOTHESIS TESTS - hypothesis_tests.py:328")
    print("= - hypothesis_tests.py:329"*80)
    
    # Hypothesis 1: Province risk differences
    print("\n📊 Testing H₀: No risk differences across provinces - hypothesis_tests.py:332")
    print("" * 40)
    # Compare Somali (highest risk) vs Addis Ababa (baseline)
    tester.test_claim_frequency('Province', 'Addis Ababa', 'Somali', 
                                 "H₀: No risk difference between Addis Ababa and Somali")
    tester.test_claim_severity('Province', 'Addis Ababa', 'Somali',
                               "H₀: No severity difference between Addis Ababa and Somali")
    
    # Hypothesis 2: Zip code risk differences
    print("\n📊 Testing H₀: No risk differences between zip codes - hypothesis_tests.py:341")
    print("" * 40)
    # Find most common zip codes for comparison
    top_zips = df['ZipCode'].value_counts().head(3).index.tolist()
    if len(top_zips) >= 2:
        tester.test_claim_frequency('ZipCode', top_zips[0], top_zips[1],
                                     f"H₀: No risk difference between Zip {top_zips[0]} and {top_zips[1]}")
        tester.test_claim_severity('ZipCode', top_zips[0], top_zips[1],
                                   f"H₀: No severity difference between Zip {top_zips[0]} and {top_zips[1]}")
    
    # Hypothesis 3: Margin difference between zip codes
    print("\n📊 Testing H₀: No margin difference between zip codes - hypothesis_tests.py:352")
    print("" * 40)
    if len(top_zips) >= 2:
        tester.test_margin('ZipCode', top_zips[0], top_zips[1],
                          f"H₀: No margin difference between Zip {top_zips[0]} and {top_zips[1]}")
    
    # Hypothesis 4: Gender risk differences
    print("\n📊 Testing H₀: No risk difference between Women and Men - hypothesis_tests.py:359")
    print("" * 40)
    tester.test_claim_frequency('Gender', 'Male', 'Female',
                                 "H₀: No risk difference between Male and Female")
    tester.test_claim_severity('Gender', 'Male', 'Female',
                               "H₀: No severity difference between Male and Female")
    
    return tester


if __name__ == "__main__":
    # Test the module
    print("Hypothesis Testing Module Loaded Successfully - hypothesis_tests.py:371")
    print("Available functions: - hypothesis_tests.py:372")
    print("HypothesisTester(df, alpha=0.05) - hypothesis_tests.py:373")
    print("run_all_hypothesis_tests(df) - hypothesis_tests.py:374")