import pandas as pd
from compare_models import train_model_linear_regression, train_model_random_forest_regressor, train_model_xgbregressor, train_model_linear_gam


def test_linear_regression_training():
    data = pd.DataFrame({
        "lat": [52.1, 52.2, 52.3, 52.4],
        "lon": [21.0, 21.1, 21.2, 21.3],
        "stop": [1, 2, 1, 0],
        "cost": [10000, 12000, 11000, 9000],
    })

    model, mse, coeffs = train_model_linear_regression(data)

    assert mse >= 0
    assert "Feature" in coeffs.columns
    assert len(coeffs) == 3


def test_random_forest_regressor():
    data = pd.DataFrame({
        "lat": [52.1, 52.2, 52.3, 52.4],
        "lon": [21.0, 21.1, 21.2, 21.3],
        "stop": [1, 2, 1, 0],
        "cost": [10000, 12000, 11000, 9000],
    })

    model, mse, coeffs = train_model_random_forest_regressor(data)

    assert mse >= 0
    assert "Feature" in coeffs.columns
    assert len(coeffs) == 3


def test_xgbregressor():
    data = pd.DataFrame({
        "lat": [52.1, 52.2, 52.3, 52.4],
        "lon": [21.0, 21.1, 21.2, 21.3],
        "stop": [1, 2, 1, 0],
        "cost": [10000, 12000, 11000, 9000],
    })

    model, mse, coeffs = train_model_xgbregressor(data)

    assert mse >= 0
    assert "Feature" in coeffs.columns
    assert len(coeffs) == 3


def test_linear_gam():
    data = pd.DataFrame({
        "lat": [52.1, 52.2, 52.3, 52.4],
        "lon": [21.0, 21.1, 21.2, 21.3],
        "stop": [1, 2, 1, 0],
        "cost": [10000, 12000, 11000, 9000],
    })

    model, mse, coeffs = train_model_linear_gam(data)

    assert mse >= 0
    assert "Feature" in coeffs.columns
    assert len(coeffs) == 3
