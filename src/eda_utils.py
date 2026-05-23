"""EDA utilities for insurance data analysis"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Optional

class EDAAnalyzer:
"""Exploratory Data Analysis utilities for insurance data"""

def init(self, data: pd.DataFrame):
self.data = data

def calculate_loss_ratio(self) -> float:
"""Calculate overall portfolio loss ratio"""
total_premium = self.data['TotalPremium'].sum()
total_claims = self.data['TotalClaims'].sum()
return total_claims / total_premium if total_premium > 0 else 0

def loss_ratio_by_group(self, group_col: str) -> pd.DataFrame:
"""Calculate loss ratio by categorical group"""
grouped = self.data.groupby(group_col).agg({
'TotalPremium': 'sum',
'TotalClaims': 'sum'
}).reset_index()
grouped['LossRatio'] = grouped['TotalClaims'] / grouped['TotalPremium']
grouped['LossRatio'] = grouped['LossRatio'].fillna(0)
return grouped

def detect_outliers(self, column: str, method: str = 'iqr') -> Tuple[pd.Series, int]:
"""Detect outliers using IQR or Z-score method"""
if method == 'iqr':
Q1 = self.data[column].quantile(0.25)
Q3 = self.data[column].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = (self.data[column] < lower_bound) | (self.data[column] > upper_bound)
elif method == 'zscore':
z_scores = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
outliers = z_scores > 3
else:
raise ValueError("Method must be 'iqr' or 'zscore'")

return outliers, outliers.sum()

def plot_premium_vs_claims_by_zip(self, zip_col: str = 'ZipCode', figsize=(12, 6)):
"""Scatter plot of TotalPremium vs TotalClaims by ZipCode"""
if zip_col not in self.data.columns:
print(f"Column {zip_col} not found. Using index instead.")
zip_data = self.data.copy()
zip_data['temp_zip'] = pd.qcut(self.data.index, 10, labels=[f'Group_{i}' for i in range(1, 11)])
zip_col = 'temp_zip'
else:
zip_data = self.data

fig, ax = plt.subplots(figsize=figsize)

for zip_code in zip_data[zip_col].unique()[:20]:
subset = zip_data[zip_data[zip_col] == zip_code]
ax.scatter(subset['TotalPremium'], subset['TotalClaims'],
alpha=0.5, label=str(zip_code))

ax.set_xlabel('Total Premium (ZAR)')
ax.set_ylabel('Total Claims (ZAR)')
ax.set_title('Premium vs Claims by Zip Code')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
return fig

def create_correlation_matrix(self) -> pd.DataFrame:
"""Create correlation matrix for numerical features"""
numeric_cols = self.data.select_dtypes(include=[np.number]).columns
correlation_matrix = self.data[numeric_cols].corr()
return correlation_matrix

def plot_correlation_heatmap(self, figsize=(12, 8)):
"""Plot correlation heatmap"""
corr_matrix = self.create_correlation_matrix()

fig, ax = plt.subplots(figsize=figsize)
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
cmap='RdBu_r', center=0, square=True,
linewidths=0.5, ax=ax)
ax.set_title('Feature Correlation Matrix')
plt.tight_layout()
return fig

def plot_geographic_trends(self, metrics: List[str] = ['TotalPremium', 'TotalClaims']):
"""Compare insurance metrics across provinces"""
fig, axes = plt.subplots(1, len(metrics), figsize=(6 * len(metrics), 6))

if len(metrics) == 1:
axes = [axes]

for i, metric in enumerate(metrics):
provincial_data = self.data.groupby('Province')[metric].agg(['mean', 'median']).reset_index()
provincial_data_sorted = provincial_data.sort_values('mean', ascending=False)

x = range(len(provincial_data_sorted))
width = 0.35

axes[i].bar([p - width/2 for p in x], provincial_data_sorted['mean'],
width, label='Mean', alpha=0.8)
axes[i].bar([p + width/2 for p in x], provincial_data_sorted['median'],
width, label='Median', alpha=0.8)

axes[i].set_xlabel('Province')
axes[i].set_ylabel(metric)
axes[i].set_title(f'{metric} by Province')
axes[i].set_xticks(x)
axes[i].set_xticklabels(provincial_data_sorted['Province'], rotation=45, ha='right')
axes[i].legend()

plt.tight_layout()
return fig

def plot_temporal_trends(self, date_col: str = 'TransactionDate'):
"""Plot claim frequency and severity over time"""
if date_col not in self.data.columns:
print(f"Date column {date_col} not found. Using index-based aggregation.")
self.data['Month'] = pd.date_range('2014-02-01', periods=len(self.data), freq='D').month
time_col = 'Month'
else:
self.data['Month'] = pd.to_datetime(self.data[date_col]).dt.to_period('M')
time_col = 'Month'

monthly_claims = self.data.groupby(time_col).agg({
'TotalClaims': ['sum', 'mean', 'count']
}).reset_index()
monthly_claims.columns = [time_col, 'TotalClaimsSum', 'AvgClaimAmount', 'ClaimCount']

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(range(len(monthly_claims)), monthly_claims['ClaimCount'],
marker='o', linewidth=2)
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Number of Claims')
axes[0].set_title('Claim Frequency Over Time')
axes[0].grid(True, alpha=0.3)

axes[1].plot(range(len(monthly_claims)), monthly_claims['AvgClaimAmount'],
marker='s', linewidth=2, color='orange')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Average Claim Amount (ZAR)')
axes[1].set_title('Claim Severity Over Time')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
return fig

def plot_vehicle_analysis(self, top_n: int = 10):
"""Analyze vehicle makes/models with highest/lowest claim amounts"""
if 'VehicleMake' not in self.data.columns:
print("VehicleMake column not found. Generating synthetic analysis.")
return self._synthetic_vehicle_analysis()

make_claims = self.data.groupby('VehicleMake')['TotalClaims'].mean().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
top_makes = make_claims.head(top_n)
axes[0].barh(range(len(top_makes)), top_makes.values)
axes[0].set_yticks(range(len(top_makes)))
axes[0].set_yticklabels(top_makes.index)
axes[0].set_xlabel('Average Claim Amount (ZAR)')
axes[0].set_title(f'Top {top_n} Vehicle Makes by Claim Amount')

bottom_makes = make_claims.tail(top_n)
axes[1].barh(range(len(bottom_makes)), bottom_makes.values)
axes[1].set_yticks(range(len(bottom_makes)))
axes[1].set_yticklabels(bottom_makes.index)
axes[1].set_xlabel('Average Claim Amount (ZAR)')
axes[1].set_title(f'Bottom {top_n} Vehicle Makes by Claim Amount')

plt.tight_layout()
return fig

def _synthetic_vehicle_analysis(self):
"""Generate synthetic vehicle analysis for demonstration"""
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

makes = ['Toyota', 'Volkswagen', 'Ford', 'BMW', 'Mercedes',
'Audi', 'Nissan', 'Hyundai', 'Honda', 'Mazda']
claim_amounts = np.random.exponential(3000, len(makes))

sorted_idx = np.argsort(claim_amounts)

axes[0].barh(np.array(makes)[sorted_idx[-5:]], claim_amounts[sorted_idx[-5:]])
axes[0].set_title('Top 5 Makes by Claim Amount')

axes[1].barh(np.array(makes)[sorted_idx[:5]], claim_amounts[sorted_idx[:5]])
axes[1].set_title('Bottom 5 Makes by Claim Amount')

return fig

def create_insight_visualizations(data: pd.DataFrame) -> dict:
"""Create three key insight-driven visualizations"""
analyzer = EDAAnalyzer(data)

visualizations = {
'loss_ratio_by_province': None,
'premium_distribution_by_gender': None,
'risk_heatmap': None
}
Visualization 1: Loss ratio by province with premium volume overlay

fig1, ax1 = plt.subplots(figsize=(12, 6))
loss_ratio_by_province = analyzer.loss_ratio_by_group('Province')
premium_by_province = data.groupby('Province')['TotalPremium'].sum()

x = range(len(loss_ratio_by_province))
bars = ax1.bar(x, loss_ratio_by_province['LossRatio'], alpha=0.7)
ax1.set_xlabel('Province')
ax1.set_ylabel('Loss Ratio')
ax1.set_title('Loss Ratio by Province (Bar height) with Premium Volume (Color intensity)')
ax1.set_xticks(x)
ax1.set_xticklabels(loss_ratio_by_province['Province'], rotation=45)

max_premium = premium_by_province.max()
for i, bar in enumerate(bars):
province = loss_ratio_by_province.iloc[i]['Province']
norm_premium = premium_by_province[province] / max_premium
bar.set_color(plt.cm.RdYlGn_r(norm_premium))

visualizations['loss_ratio_by_province'] = fig1
Visualization 2: Premium and claims distribution by gender

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

for i, metric in enumerate(['TotalPremium', 'TotalClaims']):
data.boxplot(column=metric, by='Gender', ax=axes2[i])
axes2[i].set_title(f'{metric} Distribution by Gender')
axes2[i].set_ylabel(metric)

plt.suptitle('Premium and Claims Analysis by Gender', fontsize=14)
plt.tight_layout()
visualizations['premium_distribution_by_gender'] = fig2
Visualization 3: Risk heatmap - Loss ratio by Vehicle Type and Cover Type

fig3, ax3 = plt.subplots(figsize=(10, 8))

if 'VehicleType' in data.columns and 'CoverType' in data.columns:
pivot_data = pd.pivot_table(data,
values='TotalClaims',
index='VehicleType',
columns='CoverType',
aggfunc='mean',
fill_value=0)

im = ax3.imshow(pivot_data.values, cmap='RdYlGn_r', aspect='auto')
ax3.set_xticks(range(len(pivot_data.columns)))
ax3.set_yticks(range(len(pivot_data.index)))
ax3.set_xticklabels(pivot_data.columns, rotation=45, ha='right')
ax3.set_yticklabels(pivot_data.index)
ax3.set_xlabel('Cover Type')
ax3.set_ylabel('Vehicle Type')
ax3.set_title('Average Claim Amount Heatmap: Vehicle Type vs Cover Type')

plt.colorbar(im, ax=ax3, label='Average Claim Amount (ZAR)')
else:
ax3.text(0.5, 0.5, 'VehicleType or CoverType columns not available',
ha='center', va='center', transform=ax3.transAxes)

visualizations['risk_heatmap'] = fig3

return visualizations
