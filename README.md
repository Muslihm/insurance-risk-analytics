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
