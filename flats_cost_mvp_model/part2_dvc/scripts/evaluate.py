import json
import os

import joblib
import pandas as pd
import yaml
from sklearn.model_selection import StratifiedKFold, cross_validate


def evaluate_model():
    """
    Измеряет метрики модели на данных, выполняя кросс-валидацию
    и сохраняет результаты в JSON-файл.

    Функция:
    - Загружает параметры из params.yaml.
    - Читает датасет из 'data/initial_data.csv'.
    - Загружает обученный pipeline-модель из 'models/fitted_model.pkl'.
    - Применяет кросс-валидацию с использованием StratifiedKFold.
    - Усредняет и округляет метрики.
    - Сохраняет результаты в файл 'cv_results/cv_res.json'.

    Returns:
        None
    """

    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    data = pd.read_csv("data/initial_data.csv")

    with open("models/fitted_model.pkl", "rb") as fd:
        pipeline = joblib.load(fd)

    cv_strategy = StratifiedKFold(n_splits=params["n_splits"])
    cv_res = cross_validate(
        pipeline,
        data.drop(params["target_col"], axis=1),
        data[params["target_col"]],
        cv=cv_strategy,
        n_jobs=params["n_jobs"],
        scoring=params["metrics"],
    )

    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3)
    cv_res_serializable = {k: v.tolist() for k, v in cv_res.items()}

    os.makedirs("cv_results", exist_ok=True)
    with open("cv_results/cv_res.json", "w") as fd:
        json.dump(cv_res_serializable, fd)


if __name__ == "__main__":
    evaluate_model()
