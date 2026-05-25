"""EDA utilities for insurance data analysis"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple


class EDAAnalyzer:
    """Exploratory Data Analysis utilities for insurance data"""

    def __init__(self, data: pd.DataFrame):
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

    def plot_geographic_trends(self):
        """Compare insurance metrics across provinces"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Premium by province
        premium_by_province = self.data.groupby('Province')['TotalPremium'].mean().sort_values(ascending=False)
        premium_by_province.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Average Premium by Province')
        ax1.set_xlabel('Province')
        ax1.set_ylabel('Average Premium (ZAR)')
        ax1.tick_params(axis='x', rotation=45)

        # Claims by province
        claims_by_province = self.data.groupby('Province')['TotalClaims'].mean().sort_values(ascending=False)
        claims_by_province.plot(kind='bar', ax=ax2, color='lightcoral')
        ax2.set_title('Average Claims by Province')
        ax2.set_xlabel('Province')
        ax2.set_ylabel('Average Claims (ZAR)')
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig

    def plot_premium_vs_claims(self):
        """Scatter plot of TotalPremium vs TotalClaims"""
        fig, ax = plt.subplots(figsize=(10, 6))

        scatter = ax.scatter(self.data['TotalPremium'], self.data['TotalClaims'],
                           alpha=0.5, c=self.data.index, cmap='viridis')
        ax.set_xlabel('Total Premium (ZAR)')
        ax.set_ylabel('Total Claims (ZAR)')
        ax.set_title('Premium vs Claims Scatter Plot')

        # Add trend line
        z = np.polyfit(self.data['TotalPremium'], self.data['TotalClaims'], 1)
        p = np.poly1d(z)
        ax.plot(self.data['TotalPremium'].sort_values(),
               p(self.data['TotalPremium'].sort_values()),
               "r--", alpha=0.8, label='Trend line')
        ax.legend()

        plt.colorbar(scatter, label='Policy Index')
        return fig

    def plot_temporal_trends(self, date_col=None):
        """Plot claim frequency and severity over time"""
        if date_col and date_col in self.data.columns:
            self.data['Date'] = pd.to_datetime(self.data[date_col])
            self.data['Month'] = self.data['Date'].dt.to_period('M')
        else:
            # Create synthetic dates if not available
            self.data['Date'] = pd.date_range('2014-02-01', periods=len(self.data), freq='D')
            self.data['Month'] = self.data['Date'].dt.to_period('M')

        monthly_data = self.data.groupby('Month').agg({
            'TotalClaims': ['count', 'mean']
        }).reset_index()
        monthly_data.columns = ['Month', 'ClaimCount', 'AvgClaimAmount']

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Claim frequency
        ax1.plot(range(len(monthly_data)), monthly_data['ClaimCount'],
                marker='o', linewidth=2, markersize=6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Number of Claims')
        ax1.set_title('Claim Frequency Over Time')
        ax1.grid(True, alpha=0.3)

        # Claim severity
        ax2.plot(range(len(monthly_data)), monthly_data['AvgClaimAmount'],
                marker='s', linewidth=2, markersize=6, color='orange')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Average Claim Amount (ZAR)')
        ax2.set_title('Claim Severity Over Time')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_vehicle_risk_analysis(self, top_n=10):
        """Analyze which vehicle makes have highest/lowest claim amounts"""
        if 'VehicleMake' not in self.data.columns:
            print("VehicleMake column not found - eda_utils.py:132")
            return None

        vehicle_risk = self.data.groupby('VehicleMake').agg({
            'TotalClaims': ['mean', 'count', 'std']
        }).round(2)
        vehicle_risk.columns = ['AvgClaim', 'PolicyCount', 'StdDev']
        vehicle_risk = vehicle_risk.sort_values('AvgClaim', ascending=False)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Highest risk vehicles
        top_risk = vehicle_risk.head(top_n)
        ax1.barh(range(len(top_risk)), top_risk['AvgClaim'])
        ax1.set_yticks(range(len(top_risk)))
        ax1.set_yticklabels(top_risk.index)
        ax1.set_xlabel('Average Claim Amount (ZAR)')
        ax1.set_title(f'Top {top_n} Highest Risk Vehicle Makes')

        # Lowest risk vehicles (with at least 10 policies)
        low_risk = vehicle_risk[vehicle_risk['PolicyCount'] >= 10].tail(top_n)
        ax2.barh(range(len(low_risk)), low_risk['AvgClaim'])
        ax2.set_yticks(range(len(low_risk)))
        ax2.set_yticklabels(low_risk.index)
        ax2.set_xlabel('Average Claim Amount (ZAR)')
        ax2.set_title(f'Top {top_n} Lowest Risk Vehicle Makes')

        plt.tight_layout()
        return fig


def create_insight_visualizations(data: pd.DataFrame) -> dict:
    """Create three key insight-driven visualizations"""
    analyzer = EDAAnalyzer(data)

    visualizations = {
        'loss_ratio_by_province': None,
        'premium_distribution_by_gender': None,
        'risk_heatmap': None
    }

    # Visualization 1: Loss ratio by province with premium volume overlay
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

    # Visualization 2: Premium and claims distribution by gender
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))

    for i, metric in enumerate(['TotalPremium', 'TotalClaims']):
        if 'Gender' in data.columns:
            data.boxplot(column=metric, by='Gender', ax=axes2[i])
            axes2[i].set_title(f'{metric} Distribution by Gender')
            axes2[i].set_ylabel(metric)

    plt.suptitle('Premium and Claims Analysis by Gender', fontsize=14)
    plt.tight_layout()
    visualizations['premium_distribution_by_gender'] = fig2

    # Visualization 3: Risk heatmap
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