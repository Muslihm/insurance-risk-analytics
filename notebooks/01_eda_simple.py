"""
Simple EDA Analysis - Task 1
"""

import sys
sys.path.append('..')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create sample data directly (no imports needed)
np.random.seed(42)
n_samples = 1000

provinces = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Mpumalanga']
genders = ['Male', 'Female']

df = pd.DataFrame({
    'PolicyID': range(1, n_samples + 1),
    'Province': np.random.choice(provinces, n_samples),
    'Gender': np.random.choice(genders, n_samples),
    'TotalPremium': np.random.uniform(2000, 8000, n_samples),
    'TotalClaims': np.random.exponential(500, n_samples),
})

print("= - 01_eda_simple.py:26" * 60)
print("TASK 1: EXPLORATORY DATA ANALYSIS - 01_eda_simple.py:27")
print("= - 01_eda_simple.py:28" * 60)

# 1. Loss Ratio Analysis
print("\n1. LOSS RATIO ANALYSIS - 01_eda_simple.py:31")
print("" * 40)

total_premium = df['TotalPremium'].sum()
total_claims = df['TotalClaims'].sum()
loss_ratio = total_claims / total_premium

print(f"Total Premium: R{total_premium:,.2f} - 01_eda_simple.py:38")
print(f"Total Claims: R{total_claims:,.2f} - 01_eda_simple.py:39")
print(f"Overall Loss Ratio: {loss_ratio:.2%} - 01_eda_simple.py:40")

# Loss ratio by province
print("\nLoss Ratio by Province: - 01_eda_simple.py:43")
for province in df['Province'].unique():
    province_data = df[df['Province'] == province]
    province_premium = province_data['TotalPremium'].sum()
    province_claims = province_data['TotalClaims'].sum()
    province_loss = province_claims / province_premium if province_premium > 0 else 0
    print(f"{province:20s}: {province_loss:.2%} - 01_eda_simple.py:49")

# Loss ratio by gender
print("\nLoss Ratio by Gender: - 01_eda_simple.py:52")
for gender in df['Gender'].unique():
    gender_data = df[df['Gender'] == gender]
    gender_premium = gender_data['TotalPremium'].sum()
    gender_claims = gender_data['TotalClaims'].sum()
    gender_loss = gender_claims / gender_premium if gender_premium > 0 else 0
    print(f"{gender:20s}: {gender_loss:.2%} - 01_eda_simple.py:58")

# 2. Distribution Analysis
print("\n2. DISTRIBUTION ANALYSIS - 01_eda_simple.py:61")
print("" * 40)

print(f"\nTotalPremium Statistics: - 01_eda_simple.py:64")
print(f"Mean: R{df['TotalPremium'].mean():,.2f} - 01_eda_simple.py:65")
print(f"Median: R{df['TotalPremium'].median():,.2f} - 01_eda_simple.py:66")
print(f"Min: R{df['TotalPremium'].min():,.2f} - 01_eda_simple.py:67")
print(f"Max: R{df['TotalPremium'].max():,.2f} - 01_eda_simple.py:68")

print(f"\nTotalClaims Statistics: - 01_eda_simple.py:70")
print(f"Mean: R{df['TotalClaims'].mean():,.2f} - 01_eda_simple.py:71")
print(f"Median: R{df['TotalClaims'].median():,.2f} - 01_eda_simple.py:72")
print(f"Min: R{df['TotalClaims'].min():,.2f} - 01_eda_simple.py:73")
print(f"Max: R{df['TotalClaims'].max():,.2f} - 01_eda_simple.py:74")

# 3. Outlier Detection
print("\n3. OUTLIER DETECTION - 01_eda_simple.py:77")
print("" * 40)

# IQR method for TotalPremium
Q1 = df['TotalPremium'].quantile(0.25)
Q3 = df['TotalPremium'].quantile(0.75)
IQR = Q3 - Q1
premium_outliers = df[(df['TotalPremium'] < Q1 - 1.5*IQR) | (df['TotalPremium'] > Q3 + 1.5*IQR)]
print(f"TotalPremium outliers: {len(premium_outliers)} ({len(premium_outliers)/len(df)*100:.1f}%) - 01_eda_simple.py:85")

# IQR method for TotalClaims
Q1 = df['TotalClaims'].quantile(0.25)
Q3 = df['TotalClaims'].quantile(0.75)
IQR = Q3 - Q1
claims_outliers = df[(df['TotalClaims'] < Q1 - 1.5*IQR) | (df['TotalClaims'] > Q3 + 1.5*IQR)]
print(f"TotalClaims outliers: {len(claims_outliers)} ({len(claims_outliers)/len(df)*100:.1f}%) - 01_eda_simple.py:92")

# 4. Create Visualizations
print("\n4. CREATING VISUALIZATIONS - 01_eda_simple.py:95")
print("" * 40)

# Create figures directory
import os
os.makedirs('reports/figures', exist_ok=True)

# Figure 1: Loss Ratio by Province
fig1, ax1 = plt.subplots(figsize=(10, 6))
province_loss = []
for province in df['Province'].unique():
    province_data = df[df['Province'] == province]
    province_premium = province_data['TotalPremium'].sum()
    province_claims = province_data['TotalClaims'].sum()
    province_loss_ratio = province_claims / province_premium if province_premium > 0 else 0
    province_loss.append((province, province_loss_ratio))

province_loss.sort(key=lambda x: x[1], reverse=True)
provinces, loss_ratios = zip(*province_loss)

bars = ax1.bar(range(len(provinces)), loss_ratios)
ax1.set_xticks(range(len(provinces)))
ax1.set_xticklabels(provinces, rotation=45, ha='right')
ax1.set_xlabel('Province')
ax1.set_ylabel('Loss Ratio')
ax1.set_title('Loss Ratio by Province')
ax1.axhline(y=loss_ratio, color='r', linestyle='--', label=f'Overall: {loss_ratio:.2%}')
ax1.legend()
plt.tight_layout()
fig1.savefig('reports/figures/loss_ratio_by_province.png', dpi=100, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/loss_ratio_by_province.png - 01_eda_simple.py:126")

# Figure 2: Premium Distribution by Gender
fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 5))
df.boxplot(column='TotalPremium', by='Gender', ax=ax2)
ax2.set_title('Premium Distribution by Gender')
ax2.set_ylabel('Total Premium (ZAR)')
df.boxplot(column='TotalClaims', by='Gender', ax=ax3)
ax3.set_title('Claims Distribution by Gender')
ax3.set_ylabel('Total Claims (ZAR)')
plt.suptitle('Risk Analysis by Gender')
plt.tight_layout()
fig2.savefig('reports/figures/gender_analysis.png', dpi=100, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/gender_analysis.png - 01_eda_simple.py:140")

# Figure 3: Premium vs Claims Scatter Plot
fig3, ax4 = plt.subplots(figsize=(10, 6))
scatter = ax4.scatter(df['TotalPremium'], df['TotalClaims'], alpha=0.5, c=df.index, cmap='viridis')
ax4.set_xlabel('Total Premium (ZAR)')
ax4.set_ylabel('Total Claims (ZAR)')
ax4.set_title('Premium vs Claims Analysis')
plt.colorbar(scatter, label='Policy Index')
plt.tight_layout()
fig3.savefig('reports/figures/premium_vs_claims.png', dpi=100, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/premium_vs_claims.png - 01_eda_simple.py:152")

print("\n - 01_eda_simple.py:154" + "=" * 60)
print("✅ EDA ANALYSIS COMPLETE! - 01_eda_simple.py:155")
print("= - 01_eda_simple.py:156" * 60)
print("\nKey Findings: - 01_eda_simple.py:157")
print("1. Overall portfolio loss ratio: {:.2%} - 01_eda_simple.py:158".format(loss_ratio))
print("2. Highest risk province: {} - 01_eda_simple.py:159".format(province_loss[0][0]))
print("3. Lowest risk province: {} - 01_eda_simple.py:160".format(province_loss[-1][0]))
print("\nRecommendations: - 01_eda_simple.py:161")
print("Focus marketing on lowrisk provinces for premium reduction - 01_eda_simple.py:162")
print("Review pricing strategy for highrisk segments - 01_eda_simple.py:163")
print("Investigate outlier policies for potential fraud - 01_eda_simple.py:164")