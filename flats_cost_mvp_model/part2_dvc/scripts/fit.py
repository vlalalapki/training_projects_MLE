import os

import joblib
import pandas as pd
import yaml
from catboost import CatBoostRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def fit_model():
    """
    Обучает модель регрессии на основе CatBoost и сохраняет её в виде sklearn Pipeline.

    Функция:
    - Загружает параметры из файла params.yaml.
    - Читает исходные данные из файла 'data/initial_data.csv'.
    - Преобразует признак 'building_type_int' в категориальный тип.
    - Применяет OneHotEncoding к категориальным признакам.
    - Обучает модель CatBoostRegressor.
    - Оборачивает предобработку и модель в sklearn Pipeline.
    - Сохраняет обученный pipeline в файл 'models/fitted_model.pkl'.

    Returns:
        None
    """
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    data = pd.read_csv("data/initial_data.csv")

    data = data.astype({"building_type_int": "object"})

    cat_features = data.select_dtypes(include="object")

    preprocessor =  (
        [
            (
                "category",
                OneHotEncoder(drop=params["one_hot_drop"]),
                cat_features.columns.tolist(),
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    model = CatBoostRegressor(loss_function=params["loss_function"])

    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
    pipeline.fit(data.drop(params["target_col"], axis=1), data[params["target_col"]])

    os.makedirs("models", exist_ok=True)
    with open("models/fitted_model.pkl", "wb") as fd:
        joblib.dump(pipeline, fd)


if __name__ == "__main__":
    fit_model()
