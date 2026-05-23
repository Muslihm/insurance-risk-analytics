import pytest
import pandas as pd
from src.eda_utils import EDAAnalyzer
from src.data_loader import create_sample_data
def test_loss_ratio_calculation():
    df = create_sample_data()
    analyzer = EDAAnalyzer(df)
    loss_ratio = analyzer.calculate_loss_ratio()
    assert 0 <= loss_ratio <= 1
def test_outlier_detection():
    df = create_sample_data()
    analyzer = EDAAnalyzer(df)
    outliers, count = analyzer.detect_outliers('TotalPremium')
    assert isinstance(count, int)
    assert count >= 0
