"""
Create visualizations for real insurance data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory
os.makedirs('reports/figures', exist_ok=True)

# Load data
df = pd.read_csv('data/insurance_data.csv')
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("Creating visualizations... - real_data_viz.py:22")

# Figure 1: Loss Ratio by Province
fig1, ax1 = plt.subplots(figsize=(12, 6))
province_data = df.groupby('Province').agg({
    'TotalPremium': 'sum',
    'TotalClaims': 'sum'
}).reset_index()
province_data['LossRatio'] = province_data['TotalClaims'] / province_data['TotalPremium']
province_data = province_data.sort_values('LossRatio', ascending=False)

colors = plt.cm.RdYlGn_r(province_data['LossRatio'] / province_data['LossRatio'].max())
bars = ax1.bar(range(len(province_data)), province_data['LossRatio'], color=colors)
ax1.set_xticks(range(len(province_data)))
ax1.set_xticklabels(province_data['Province'], rotation=45, ha='right')
ax1.set_xlabel('Province')
ax1.set_ylabel('Loss Ratio')
ax1.set_title('Loss Ratio by Province (Green = Lower Risk, Red = Higher Risk)')
ax1.axhline(y=province_data['LossRatio'].mean(), color='blue', linestyle='--', 
            label=f'Average: {province_data["LossRatio"].mean():.2%}')
ax1.legend()
plt.tight_layout()
fig1.savefig('reports/figures/loss_ratio_by_province.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/loss_ratio_by_province.png - real_data_viz.py:46")

# Figure 2: Premium Distribution by Vehicle Type
fig2, ax2 = plt.subplots(figsize=(12, 6))
vehicle_types = df.groupby('VehicleType')['TotalPremium'].mean().sort_values(ascending=False)
vehicle_types.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_xlabel('Vehicle Type')
ax2.set_ylabel('Average Premium (ETB)')
ax2.set_title('Average Premium by Vehicle Type')
ax2.tick_params(axis='x', rotation=45)
plt.tight_layout()
fig2.savefig('reports/figures/premium_by_vehicle.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/premium_by_vehicle.png - real_data_viz.py:59")

# Figure 3: Claim Frequency by Age Group
fig3, ax3 = plt.subplots(figsize=(10, 6))
df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 25, 35, 50, 65, 100], 
                         labels=['18-25', '26-35', '36-50', '51-65', '65+'])
claim_freq = df.groupby('AgeGroup').apply(lambda x: (x['TotalClaims'] > 0).mean())
claim_freq.plot(kind='bar', ax=ax3, color='coral')
ax3.set_xlabel('Age Group')
ax3.set_ylabel('Claim Frequency')
ax3.set_title('Claim Frequency by Age Group')
ax3.set_ylim(0, max(claim_freq) * 1.2)
plt.tight_layout()
fig3.savefig('reports/figures/claim_frequency_by_age.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/claim_frequency_by_age.png - real_data_viz.py:74")

# Figure 4: Premium vs Claims Scatter
fig4, ax4 = plt.subplots(figsize=(12, 8))
scatter = ax4.scatter(df['TotalPremium'], df['TotalClaims'], 
                     alpha=0.5, c=df['Age'], cmap='viridis', s=20)
ax4.set_xlabel('Total Premium (ETB)')
ax4.set_ylabel('Total Claims (ETB)')
ax4.set_title('Premium vs Claims (Color = Age)')
plt.colorbar(scatter, ax=ax4, label='Age')
plt.tight_layout()
fig4.savefig('reports/figures/premium_vs_claims.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/premium_vs_claims.png - real_data_viz.py:87")

# Figure 5: Risk Heatmap - Province vs Cover Type
fig5, ax5 = plt.subplots(figsize=(10, 8))
pivot_data = pd.pivot_table(df, 
                           values='TotalClaims', 
                           index='Province', 
                           columns='CoverType', 
                           aggfunc='mean',
                           fill_value=0)
im = ax5.imshow(pivot_data.values, cmap='RdYlGn_r', aspect='auto')
ax5.set_xticks(range(len(pivot_data.columns)))
ax5.set_yticks(range(len(pivot_data.index)))
ax5.set_xticklabels(pivot_data.columns, rotation=45, ha='right')
ax5.set_yticklabels(pivot_data.index)
ax5.set_xlabel('Cover Type')
ax5.set_ylabel('Province')
ax5.set_title('Average Claim Amount Heatmap: Province vs Cover Type')
plt.colorbar(im, ax=ax5, label='Average Claim (ETB)')
plt.tight_layout()
fig5.savefig('reports/figures/risk_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: reports/figures/risk_heatmap.png - real_data_viz.py:109")

print("\n✅ All visualizations created successfully! - real_data_viz.py:111")
print("📁 Figures saved in: reports/figures/ - real_data_viz.py:112")