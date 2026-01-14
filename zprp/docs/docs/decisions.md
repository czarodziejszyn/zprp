# Choosing models for price prediction

When choosing models for our application we had to keep in mind two main aspects: models had to be capable of performing high-precision regression and we had to be able to see influence of individual features, which for example eliminates neural networks which would probably perform better.

## Linear Regression

This model was chosen as a baseline for other models to see if more complex models are actually adding value. It was the simplest model and the most transparent one where each factor has specific coefficient so it shows its direct global influence.

## Random Forest Regressor

This model was selected to capture non-linear dependencies and interactions between variables that a simple linear model might miss. Random forest regressor builds multiple decision trees which are good at handling noisy data - like ours. This is most likely the reason why this model performed best out of all 4.

## Extreme Gradient Boosting

This model was chosen to achieve the highest possible accuracy by iteratively refining errors. It builds trees like previous model, but builds them sequentially where each new tree focuses on correcting error of the previous ones. It performed very similarly as random forest regressor but a bit worse.

## Linear GAM (Generalized Additive Model)

This was the only models we have not used previously, so it was chosen as an experiment but also because it allows for non-linear smooths so it can model relations that are not straight lines but still mathematically continuous and easy to visualize.

## Results

We tested these models 4 models on 3 different datasets. Each dataset had different radius (different distance from which objects used for prediction were counted).

| Model | 300m radius | 500m radius | 700m radius |
| :--- | :--- | :--- | :--- |
| **LinearGAM** | 4.073059e+07 | 4.017767e+07 | 5.003699e+07 |
| **LinearRegression** | 5.090107e+07 | 4.612010e+07 | 4.679640e+07 |
| **RandomForestRegressor** | 3.374867e+07 | 3.420113e+07 | 3.372151e+07 |
| **XGBRegressor** | 3.478991e+07 | 3.522379e+07 | 3.425711e+07 |

As the above table shows model with the lowest mean squared error was RandomForestRegressor on 700m radius dataset.
