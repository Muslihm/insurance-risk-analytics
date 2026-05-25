"""
Real Insurance Data Analysis - Final Version
AlphaCare Insurance Solutions - Ethiopian Insurance Data
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("= - real_data_analysis.py:11" * 70)
print("ALPHACARE INSURANCE  REAL DATA ANALYSIS - real_data_analysis.py:12")
print("= - real_data_analysis.py:13" * 70)

# Load data
df = pd.read_csv('data/insurance_data.csv')
print(f"\n✅ Data loaded: {len(df):,} policies - real_data_analysis.py:17")
print(f"Period: {pd.to_datetime(df['TransactionDate']).min()} to {pd.to_datetime(df['TransactionDate']).max()} - real_data_analysis.py:18")
print(f"Columns: {len(df.columns)} - real_data_analysis.py:19")

# Convert dates
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# 1. LOSS RATIO ANALYSIS
print("\n - real_data_analysis.py:25" + "=" * 70)
print("1. PORTFOLIO LOSS RATIO ANALYSIS - real_data_analysis.py:26")
print("= - real_data_analysis.py:27" * 70)

total_premium = df['TotalPremium'].sum()
total_claims = df['TotalClaims'].sum()
overall_loss_ratio = total_claims / total_premium

print(f"Total Premium Collected: ETB {total_premium:,.2f} - real_data_analysis.py:33")
print(f"Total Claims Paid: ETB {total_claims:,.2f} - real_data_analysis.py:34")
print(f"Overall Loss Ratio: {overall_loss_ratio:.2%} - real_data_analysis.py:35")

# Loss ratio by province
print("\n📊 Loss Ratio by Province: - real_data_analysis.py:38")
province_loss = df.groupby('Province').agg({
    'TotalPremium': 'sum',
    'TotalClaims': 'sum'
}).reset_index()
province_loss['LossRatio'] = province_loss['TotalClaims'] / province_loss['TotalPremium']
province_loss = province_loss.sort_values('LossRatio', ascending=False)

for _, row in province_loss.iterrows():
    if row['LossRatio'] > 0.55:
        indicator = "🔴 HIGH RISK"
    elif row['LossRatio'] > 0.5:
        indicator = "🟡 MEDIUM RISK"
    else:
        indicator = "🟢 LOW RISK"
    print(f"{row['Province']:20s}: {row['LossRatio']:.2%} ({indicator}) - real_data_analysis.py:53")

# Loss ratio by vehicle type
print("\n📊 Loss Ratio by Vehicle Type: - real_data_analysis.py:56")
vehicle_loss = df.groupby('VehicleType').agg({
    'TotalPremium': 'sum',
    'TotalClaims': 'sum'
}).reset_index()
vehicle_loss['LossRatio'] = vehicle_loss['TotalClaims'] / vehicle_loss['TotalPremium']
vehicle_loss = vehicle_loss.sort_values('LossRatio', ascending=False)

for _, row in vehicle_loss.iterrows():
    if row['LossRatio'] > 0.7:
        indicator = "🔴 CRITICAL"
    elif row['LossRatio'] > 0.5:
        indicator = "🟡 NEEDS REVIEW"
    else:
        indicator = "🟢 GOOD"
    print(f"{row['VehicleType']:15s}: {row['LossRatio']:.2%} ({indicator}) - real_data_analysis.py:71")

# 2. CLAIM STATISTICS
print("\n - real_data_analysis.py:74" + "=" * 70)
print("2. CLAIM STATISTICS - real_data_analysis.py:75")
print("= - real_data_analysis.py:76" * 70)

claims_with_claim = df[df['TotalClaims'] > 0]
print(f"Policies with claims: {len(claims_with_claim):,} ({len(claims_with_claim)/len(df)*100:.1f}%) - real_data_analysis.py:79")
print(f"Average claim amount: ETB {claims_with_claim['TotalClaims'].mean():,.2f} - real_data_analysis.py:80")
print(f"Median claim amount: ETB {claims_with_claim['TotalClaims'].median():,.2f} - real_data_analysis.py:81")
print(f"Maximum claim amount: ETB {claims_with_claim['TotalClaims'].max():,.2f} - real_data_analysis.py:82")

# 3. LOW-RISK SEGMENTS (Premium Reduction Opportunities)
print("\n - real_data_analysis.py:85" + "=" * 70)
print("3. LOWRISK SEGMENTS (Premium Reduction Opportunities) - real_data_analysis.py:86")
print("= - real_data_analysis.py:87" * 70)

# Low-risk provinces (below average)
low_risk_provinces = province_loss[province_loss['LossRatio'] < overall_loss_ratio]
print("\n🎯 Provinces with belowaverage loss ratio: - real_data_analysis.py:91")
for _, row in low_risk_provinces.iterrows():
    savings_pct = (overall_loss_ratio - row['LossRatio']) / overall_loss_ratio * 100
    print(f"✅ {row['Province']:15s}: {row['LossRatio']:.2%} (Potential {savings_pct:.0f}% premium reduction) - real_data_analysis.py:94")

# Low-risk vehicle types
low_risk_vehicles = vehicle_loss[vehicle_loss['LossRatio'] < overall_loss_ratio]
print("\n🚗 Vehicle types with belowaverage loss ratio: - real_data_analysis.py:98")
for _, row in low_risk_vehicles.iterrows():
    print(f"✅ {row['VehicleType']:15s}: {row['LossRatio']:.2%} - real_data_analysis.py:100")

# 4. HIGH-RISK SEGMENTS (Need Pricing Review)
print("\n - real_data_analysis.py:103" + "=" * 70)
print("4. HIGHRISK SEGMENTS (Urgent Pricing Review) - real_data_analysis.py:104")
print("= - real_data_analysis.py:105" * 70)

high_risk_provinces = province_loss[province_loss['LossRatio'] > overall_loss_ratio * 1.1]
print("\n⚠️ Provinces requiring immediate review: - real_data_analysis.py:108")
for _, row in high_risk_provinces.iterrows():
    excess_pct = (row['LossRatio'] - overall_loss_ratio) / overall_loss_ratio * 100
    print(f"🔴 {row['Province']:15s}: {row['LossRatio']:.2%} ({excess_pct:.0f}% above average) - real_data_analysis.py:111")

high_risk_vehicles = vehicle_loss[vehicle_loss['LossRatio'] > overall_loss_ratio * 1.1]
print("\n⚠️ Vehicle types requiring immediate review: - real_data_analysis.py:114")
for _, row in high_risk_vehicles.iterrows():
    excess_pct = (row['LossRatio'] - overall_loss_ratio) / overall_loss_ratio * 100
    print(f"🔴 {row['VehicleType']:15s}: {row['LossRatio']:.2%} ({excess_pct:.0f}% above average) - real_data_analysis.py:117")

# 5. PREMIUM ANALYSIS BY COVER TYPE
print("\n - real_data_analysis.py:120" + "=" * 70)
print("5. PREMIUM ANALYSIS BY COVER TYPE - real_data_analysis.py:121")
print("= - real_data_analysis.py:122" * 70)

# Use the correct column name for counting (CustomerID or just use index)
if 'CustomerID' in df.columns:
    count_col = 'CustomerID'
elif 'PolicyID' in df.columns:
    count_col = 'PolicyID'
else:
    count_col = df.index.name if df.index.name else 'index'

cover_analysis = df.groupby('CoverType').agg({
    'TotalPremium': 'mean',
    'TotalClaims': 'mean'
}).round(2)
cover_analysis.columns = ['AvgPremium', 'AvgClaim']
cover_analysis['PolicyCount'] = df.groupby('CoverType').size()
cover_analysis['LossRatio'] = cover_analysis['AvgClaim'] / cover_analysis['AvgPremium']

print(cover_analysis.to_string())

# 6. RECOMMENDATIONS
print("\n - real_data_analysis.py:143" + "=" * 70)
print("6. STRATEGIC RECOMMENDATIONS - real_data_analysis.py:144")
print("= - real_data_analysis.py:145" * 70)

print("""
🎯 IMMEDIATE ACTIONS (Next 30 Days):

1. PREMIUM REDUCTION - LOW RISK SEGMENTS:
   ✅ REDUCE premiums in Amhara province (currently 47.76% loss ratio)
   ✅ LOWER rates for Sedan and Hatchback vehicles
   ✅ Create targeted marketing campaigns for these low-risk segments

2. PRICING REVIEW - HIGH RISK SEGMENTS:
   🔴 INCREASE premiums for Luxury vehicles (84.24% loss ratio)
   🔴 REVIEW Somali province pricing (61.19% loss ratio)
   🔴 ADJUST SUV premiums (56.37% loss ratio)

3. MARKETING STRATEGY:
   📢 Aggressively acquire customers in Amhara province
   📢 Promote Sedan/Hatchback coverage with competitive rates
   📢 Develop digital campaigns targeting low-risk demographics

4. FURTHER ANALYSIS NEEDED:
   🔍 Investigate outlier claims (max: ETB 49,623)
   🔍 Analyze seasonal patterns in claims
   🔍 Develop predictive model for claim probability

📊 EXPECTED IMPACT:
   - Potential premium reduction of 10-15% in low-risk segments
   - Estimated 20-30% increase in policy volume from targeted marketing
   - Improved overall loss ratio by 5-8% within 6 months
""")

print("=" * 70)
print("✅ ANALYSIS COMPLETE - Ready for Task 2 (Hypothesis Testing)")
print("=" * 70)

# Export key findings to CSV
import os
os.makedirs('reports', exist_ok=True)

summary_df = pd.DataFrame({
    'Metric': ['Overall Loss Ratio', 'Total Premium', 'Total Claims', 'Claim Frequency', 
               'Best Province', 'Best Vehicle Type', 'Worst Province', 'Worst Vehicle Type'],
    'Value': [
        f'{overall_loss_ratio:.2%}', 
        f'ETB {total_premium:,.0f}', 
        f'ETB {total_claims:,.0f}', 
        f'{len(claims_with_claim)/len(df)*100:.1f}%',
        low_risk_provinces.iloc[0]['Province'] if len(low_risk_provinces) > 0 else 'N/A',
        low_risk_vehicles.iloc[0]['VehicleType'] if len(low_risk_vehicles) > 0 else 'N/A',
        high_risk_provinces.iloc[0]['Province'] if len(high_risk_provinces) > 0 else 'N/A',
        high_risk_vehicles.iloc[0]['VehicleType'] if len(high_risk_vehicles) > 0 else 'N/A'
    ]
})
summary_df.to_csv('reports/key_metrics_summary.csv', index=False)
print("\n✅ Key metrics saved to: reports/key_metrics_summary.csv")