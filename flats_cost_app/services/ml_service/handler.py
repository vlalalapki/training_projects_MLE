"""Класс FastApiHandler, который обрабатывает запросы API."""

import json
import os

import constants
import dill
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {"object_id": str, "model_params": dict}

        self.model_path = constants.MODEL_PATH
        self.prep_center_path = constants.CENTER_PATH
        self.prep_afc_path = constants.AFC_PREPROCESS_PATH
        self.prep_ck_path = constants.SK_PREPROCESS_PATH
        self.prep_input_path = constants.INPUT_EXAMPLE_PATH

        self.load_churn_model(model_path=self.model_path)

        # необходимые параметры для предсказаний стоимости квартиры
        self.required_model_params = constants.REQUIRED_MODEL_PARAMS

    def load_churn_model(self, model_path: str):
        """Загружаем обученную модель регрессии.
        Args:
            model_path (str): Путь до модели.
        """
        self.model = CatBoostRegressor()
        if os.path.exists(model_path):
            self.model.load_model(model_path)
        else:
            print("Failed to load model")

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.

        Args:
            query_params (dict): Параметры запроса.

        Returns:
                bool: True — если есть нужные параметры, False — иначе
        """
        if "object_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["object_id"], self.param_types["object_id"]):
            return False

        if not isinstance(
            query_params["model_params"], self.param_types["model_params"]
        ):
            return False
        return True

    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.

        Args:
            model_params (dict): Параметры объекта для предсказания.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False

    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            - **dict**: Cловарь со всеми параметрами запроса.
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True

    def load_preprocess_tools(
        self,
        prep_center_path: str,
        prep_afc_path: str,
        prep_ck_path: str,
        prep_input_path: str,
    ):
        """Загружаем данные и модели для предобработки признаков

        Args:
            preprocess_path (str): Путь к папке с инструментами препроцессинга

        Returns:
            dict: словарь с загруженными инструментами
        """

        prep_tools = {}

        for prep_path in [
            prep_center_path,
            prep_afc_path,
            prep_ck_path,
            prep_input_path,
        ]:
            if os.path.exists(prep_path):
                print("Preprocessing path is ok")
            else:
                print("Trouble with preprocess path")

        with open(os.path.normpath(prep_center_path), "r") as fd:
            prep_tools["center"] = json.load(fd)["center"]

        with open(os.path.normpath(prep_afc_path), "rb") as fd:
            prep_tools["afc_model"] = dill.load(fd)

        with open(os.path.normpath(prep_ck_path), "rb") as fd:
            prep_tools["sk_model"] = dill.load(fd)

        with open(os.path.normpath(prep_input_path), "r") as fd:
            prep_tools["final_params"] = json.load(fd)["columns"]

        return prep_tools

    def prepare_model_params(self, model_params: dict):
        """Предобработка параметров модели перед запуском предсказания:
                - новый параметр distance_to_center
                - удаление параметров latitude и longitude
                - создание признаков через sk_preprocess и afc_preprocess
                - удаление лишних параметров согласно input_example модели

        Args:
            model_params (dict): Параметры модели

        Returns:
            pd.DataFrame: Обновленные параметры модели
        """
        try:
            prep_tools = self.load_preprocess_tools(
                self.prep_center_path,
                self.prep_afc_path,
                self.prep_ck_path,
                self.prep_input_path,
            )

            model_params["distance_to_center"] = np.linalg.norm(
                prep_tools["center"]
                - np.array(
                    [model_params.pop("latitude"), model_params.pop("longitude")]
                )
            ).round(3)

            df_model_params = pd.DataFrame([model_params])
            sk_model_params = prep_tools["sk_model"].transform(df_model_params)
            sk_model_params = pd.DataFrame(
                sk_model_params, columns=prep_tools["sk_model"].get_feature_names_out()
            )

            afc_model_params = prep_tools["afc_model"].transform(df_model_params)

            full_model_params = pd.concat([sk_model_params, afc_model_params], axis=1)

            upgrade_model_params = full_model_params[prep_tools["final_params"]]

        except Exception as e:
            print(f"Problem with preprocessing {e}")
        else:
            return upgrade_model_params

    def churn_predict(self, upgrade_model_params: pd.DataFrame) -> float:
        """Предсказываем цену на квартиру.

        Args:
            upgrade_model_params (pd.DataFrame): Подготовленные параметры для модели.

        Returns:
            float — стоимость квартиры
        """
        return self.model.predict(upgrade_model_params)

    def handle(self, params: dict):
        """Функция для обработки входящих запросов по API. Запрос состоит из параметров.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            - **dict**: Словарь, содержащий результат выполнения запроса.
        """
        try:
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                object_id = params["object_id"]
                print(
                    f"Predicting for object_id: {object_id} and model_params:\n{model_params}"
                )
                upgrade_model_params = self.prepare_model_params(model_params)
                cost = self.churn_predict(upgrade_model_params).tolist()
                response = {"object_id": object_id, "object_cost": cost}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response


if __name__ == "__main__":
    # создаём тестовый запрос
    test_params = {
        "object_id": "666",
        "model_params": {
            "floor": 5,
            "is_apartment": 0,
            "kitchen_area": 5,
            "total_area": 40,
            "build_year": 1955,
            "building_type_int": 4,
            "ceiling_height": 3,
            "flats_count": 80,
            "floors_total": 5,
            "has_elevator": 0,
            "latitude": 35,
            "longitude": 29,
        },
    }

    handler = FastApiHandler()

    response = handler.handle(test_params)
    print(f"Response: {response}")
