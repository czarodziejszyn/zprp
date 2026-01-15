# Data science

This directory contains python programs for dataset creation and comparing models and JSON files that were used for early model.

## `average_cost.json`

This file was used to create dataset before we had scraped prices for real houses. It has average price for $m^2$ per Warsaw district.

## `compare_models.py`

This file automatically compares 4 machine learning models: linear regression, random forest regressor, xgbregressor and linear gam. The models are created and trained with 3 different datasets - each with different radius - so 12 models are trained in total. Later the best model and the best radius is chosen. Trained model is saved in `zprp/models` directory and chart with its' feature importances is saved in `zprp/reports/figures` directory.

## `create_dataset.py`

This python program generates dataset and saves it. You can change radius parameter to get infrastructure object counts from different distance.

## `data_record.py`

This python file contains Data_record class that represents one record from dataset. In order for this program to work while creating dataset, backend docker must be up, so we can send http requests to get counts of infrastructure objects.

## `dataset.py`

This python file contains Dataset class, that is used for creating datasets.

## `model_comparison.txt`

This file contains output of `compare_models.py` program. It shows how different models performed on different radius datasets and shows which model and radius are best.

## `warszawa-dzielnice.geojsn`

This file was downloaded from https://github.com/andilabs/warszawa-dzielnice-geojson and was used to determine Warsaw district based on coordinates. It was used for creating datasets before we had real scraped offers.
