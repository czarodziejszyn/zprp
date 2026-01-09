import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from pygam import LinearGAM, s
from functools import reduce
import numpy as np
from sklearn.metrics import mean_squared_error
import pickle
import matplotlib.pyplot as plt


def prepare_datasets(data):
    X, y = data.drop("cost", axis=1), data["cost"]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_val, y_train, y_val


def train_model_linear_regression(data):
    X_train, X_val, y_train, y_val = prepare_datasets(data)
    model = LinearRegression()
    model.fit(X_train, y_train)
    mse = test_model(model, X_val, y_val)
    coefficients = pd.DataFrame({
        'Feature': X_train.columns,
        'Coefficient': model.coef_
    }).sort_values(by="Coefficient", ascending=False)
    return model, mse, coefficients


def train_model_random_forest_regressor(data):
    X_train, X_val, y_train, y_val = prepare_datasets(data)
    model = RandomForestRegressor(n_estimators=300)
    model.fit(X_train, y_train)
    mse = test_model(model, X_val, y_val)
    coefficients = pd.DataFrame({
        'Feature': X_train.columns,
        'Feature Importance': model.feature_importances_
    }).sort_values(by="Feature Importance", ascending=False)
    return model, mse, coefficients


def train_model_xgbregressor(data):
    X_train, X_val, y_train, y_val = prepare_datasets(data)
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5
    )
    model.fit(X_train, y_train)
    mse = test_model(model, X_val, y_val)
    coefficients = pd.DataFrame({
        'Feature': X_train.columns,
        'Feature Importance': model.feature_importances_
    }).sort_values(by="Feature Importance", ascending=False)
    return model, mse, coefficients


def train_model_linear_gam(data):
    X_train, X_val, y_train, y_val = prepare_datasets(data)
    n_features = X_train.shape[1]
    terms = reduce(lambda a, b: a + b, [s(i) for i in range(n_features)])
    model = LinearGAM(terms)
    model.gridsearch(X_train, y_train)
    mse = test_model(model, X_val, y_val)
    importances = []

    for i in range(n_features):
        _ = model.generate_X_grid(term=i)
        pdep = model.partial_dependence(term=i)
        importance = np.var(pdep)
        importances.append(importance)

    coefficients = pd.DataFrame({
        'Feature': X_train.columns,
        'Feature Importance': importances
    }).sort_values(by="Feature Importance", ascending=False)
    return model, mse, coefficients


def test_model(model, X_val, y_val):
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    return mse


if __name__ == "__main__":
    datasets = {
        "300m radius": pd.read_csv(
            "../data/processed/warsaw_house_data_300.csv", index_col=0),
        "500m radius": pd.read_csv(
            "../data/processed/warsaw_house_data_500.csv", index_col=0),
        "700m radius": pd.read_csv(
            "../data/processed/warsaw_house_data_700.csv", index_col=0)
    }

    models = {
        "LinearRegression": train_model_linear_regression,
        "RandomForestRegressor": train_model_random_forest_regressor,
        "XGBRegressor": train_model_xgbregressor,
        "LinearGAM": train_model_linear_gam
    }

    results = []

    best_mse = 999999999
    best_model = None
    best_model_name = None
    best_coeffs = None
    best_dataset = None

    for data_name, df in datasets.items():
        for model_name, model in models.items():
            model, mse, coeffs = model(df)

            if mse < best_mse:
                best_mse = mse
                best_model = model
                best_model_name = model_name
                best_coeffs = coeffs
                best_dataset = data_name

            results.append({
                "dataset": data_name,
                "model": model_name,
                "mse": mse
            })

    results_df = pd.DataFrame(results)
    comparison = results_df.pivot(
        index="model",
        columns="dataset",
        values="mse"
    )

    print(comparison)

    print(f"Best model: {best_model_name}")
    print(f"Best model MSE: {best_mse}")
    print(f"Best dataset: {best_dataset}")
    with open("../models/model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    plt.figure(figsize=(8, 5))
    plt.barh(best_coeffs["Feature"],
             best_coeffs["Feature Importance"], color='skyblue')
    plt.title("Wpływ poszczególnych cech na wynik")
    plt.xlabel('"Ważność" cechy')
    plt.ylabel("Cecha")
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(
        "../reports/figures/chart.png")
    plt.show()
