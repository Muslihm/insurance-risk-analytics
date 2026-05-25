# AlphaCare Insurance Solutions - Risk Analytics Project

## Business Overview
AlphaCare Insurance Solutions (ACIS) is developing cutting-edge risk and predictive analytics for car insurance planning and marketing in South Africa. This project analyzes 18 months of historical insurance claim data (Feb 2014 - Aug 2015) to optimize marketing strategy and identify low-risk targets for premium reduction.

## Project Objectives
- Build deep understanding of insurance risk metrics
- Statistically validate risk drivers across provinces, zip codes, and gender
- Develop predictive models for claim severity and probability
- Deliver actionable recommendations for risk-based pricing

## Repository Structure
insurance-risk-analytics/
├── .github/workflows/ # CI/CD pipeline
├── data/ # Data files (DVC tracked)
├── notebooks/ # Jupyter notebooks for analysis
├── src/ # Reusable Python modules
├── reports/ # Business-facing reports
├── tests/ # Unit tests
└── requirements.txt # Python dependencies
## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/insurance-risk-analytics.git
cd insurance-risk-analytics
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Pull Data with DVC
dvc pull
Analysis Workflow

    Task 1: EDA and Data Quality Assessment

    Task 2: Hypothesis Testing on Risk Drivers

    Task 3: Predictive Modeling
Key Metrics

    Loss Ratio = Total Claims / Total Premium

    Claim Severity = Average claim amount

    Claim Frequency = Probability of at least one claim

Team

Marketing Analytics Team, AlphaCare Insurance Solutions
## Data Version Control (DVC) Pipeline

This project uses DVC for reproducible data versioning. Below are instructions to reproduce the data pipeline.

### Prerequisites

pip install dvc pandas numpy
Setup

1. Clone the repository:

    git clone <repository-url>
    cd <project-directory>

2. Pull DVC-tracked data:

dvc pull

Data Versions
Version	       Description	                            Location
v1.0	  Raw insurance data	                data/raw/insurance_data.csv
v2.0	 Cleaned data with basic features	    data/processed/insurance_data_cleaned.csv
v3.0	 Enhanced data with additional derived features	data/processed/insurance_data_cleaned_v2.csv
Reproducing the Pipeline

To reproduce the entire data pipeline from raw data:

# Run the cleaning pipeline
dvc repro

# Or manually run the cleaning script
python scripts/clean_data.py

# Generate second version
python scripts/create_second_version.py
Data Lineage

The data pipeline consists of:

    Raw Data (data/raw/insurance_data.csv): Original insurance dataset

    Clean Stage (scripts/clean_data.py):

        Converts date types

        Creates derived features (ClaimRatio, RiskCategory, IncomeGroup)

        Handles missing values

    Enhanced Stage (scripts/create_second_version.py):

        Adds PremiumPerRisk ratio

        Creates age groups and NCD categories

        Adds claim severity classification

Switching Between Versions

To switch to a specific data version:
bash

# Checkout a specific version
git checkout v2.0

# Pull corresponding data
dvc pull

Remote Storage

Data is stored in a local DVC remote at /path/to/local/storage/. To push new versions:
bash

dvc push

To pull latest versions:
bash

dvc pull

text


## Step 8: Complete the Workflow

```bash
# Stage all changes
git add .
git commit -m "Complete DVC setup with two data versions"

# Push to remote
git push origin task-2

# Create Pull Request to merge into main
# (This would be done via GitHub/GitLab UI)

# After PR approval, merge and update local main
git checkout main
git pull origin main