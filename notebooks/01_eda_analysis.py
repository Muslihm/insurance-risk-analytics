"""
Task 1: Exploratory Data Analysis - Insurance Claims Data
Run this script instead of the notebook if Jupyter has issues
"""

import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import InsuranceDataLoader, create_sample_data
from src.eda_utils import EDAAnalyzer

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("= - 01_eda_analysis.py:19" * 60)
print("TASK 1: EXPLORATORY DATA ANALYSIS - 01_eda_analysis.py:20")
print("= - 01_eda_analysis.py:21" * 60)

# Load data
try:
    loader = InsuranceDataLoader()
    df = loader.load_data()
    print(f"✅ Real data loaded: {df.shape} - 01_eda_analysis.py:27")
except FileNotFoundError:
    print("⚠️ Real data not found. Using sample data for demonstration. - 01_eda_analysis.py:29")
    df = create_sample_data()
    print(f"✅ Sample data created: {df.shape} - 01_eda_analysis.py:31")

# Initialize analyzer
analyzer = EDAAnalyzer(df)

# 1. Loss Ratio Analysis
print("\n - 01_eda_analysis.py:37" + "=" * 60)
print("1. LOSS RATIO ANALYSIS - 01_eda_analysis.py:38")
print("= - 01_eda_analysis.py:39" * 60)

overall_loss_ratio = analyzer.calculate_loss_ratio()
print(f"Overall Portfolio Loss Ratio: {overall_loss_ratio:.2%} - 01_eda_analysis.py:42")
print(f"Total Premium Collected: R{df['TotalPremium'].sum():,.2f} - 01_eda_analysis.py:43")
print(f"Total Claims Paid: R{df['TotalClaims'].sum():,.2f} - 01_eda_analysis.py:44")

# Loss ratio by province
loss_by_province = analyzer.loss_ratio_by_group('Province')
print("\nLoss Ratio by Province: - 01_eda_analysis.py:48")
for _, row in loss_by_province.sort_values('LossRatio', ascending=False).iterrows():
    print(f"{row['Province']:20s}: {row['LossRatio']:.2%} - 01_eda_analysis.py:50")

# 2. Outlier Analysis
print("\n - 01_eda_analysis.py:53" + "=" * 60)
print("2. OUTLIER ANALYSIS - 01_eda_analysis.py:54")
print("= - 01_eda_analysis.py:55" * 60)

for col in ['TotalPremium', 'TotalClaims']:
    if col in df.columns:
        outliers, count = analyzer.detect_outliers(col)
        print(f"{col:20s}: {count:4d} outliers ({count/len(df)*100:.1f}%) - 01_eda_analysis.py:60")

# 3. Visualizations
print("\n - 01_eda_analysis.py:63" + "=" * 60)
print("3. GENERATING VISUALIZATIONS - 01_eda_analysis.py:64")
print("= - 01_eda_analysis.py:65" * 60)

# Create output directory for plots
import os
os.makedirs('reports/figures', exist_ok=True)

# Plot 1: Geographic trends
fig1 = analyzer.plot_geographic_trends()
fig1.savefig('reports/figures/geographic_trends.png', dpi=100, bbox_inches='tight')
plt.close(fig1)
print("✅ Saved: reports/figures/geographic_trends.png - 01_eda_analysis.py:75")

# Plot 2: Premium vs Claims
fig2 = analyzer.plot_premium_vs_claims()
fig2.savefig('reports/figures/premium_vs_claims.png', dpi=100, bbox_inches='tight')
plt.close(fig2)
print("✅ Saved: reports/figures/premium_vs_claims.png - 01_eda_analysis.py:81")

# Plot 3: Temporal trends
fig3 = analyzer.plot_temporal_trends()
fig3.savefig('reports/figures/temporal_trends.png', dpi=100, bbox_inches='tight')
plt.close(fig3)
print("✅ Saved: reports/figures/temporal_trends.png - 01_eda_analysis.py:87")

print("\n - 01_eda_analysis.py:89" + "=" * 60)
print("✅ EDA ANALYSIS COMPLETE! - 01_eda_analysis.py:90")
print("= - 01_eda_analysis.py:91" * 60)