# Model Inference

This module serves as the bridge between the model and the backend API. It is responsible for loading the model, processing real-time geographical data into features, and generating price predictions.

## Model Execution (run_model.py)
The module encapsulates the logic required to perform inference within a containerized Docker environment. It operates through two primary functions:
### 1. Price Prediction Logic  
The calculate_prices function performs the core estimation. It orchestrates a multi-step process to determine a property's value.
* Feature Engineering: It utilizes the DataRecord class to transform raw coordinates into a feature vector based on a chosen radius of urban infrastructure.
* Model Inference: Loads the pre-trained model (from models/model.pkl) to predict the price per m2.
* Market Comparison: Fetches the actual average market price from the database within a chosen radius to provide real-world context for the prediction.

### 2. Visualization & Reporting  
The create_chart function supports the frontend by providing visual insights into the model's decision-making process.  
* Feature Importance: It provides access to the generated visualization (located in reports/figures/chart.png) which illustrates which urban factors (e.g., proximity to parks or transport) had the most significant impact on the final price estimation.

## Technical Reference
The module interacts with both the data_science package for record processing and the db module for fetching historical market averages.