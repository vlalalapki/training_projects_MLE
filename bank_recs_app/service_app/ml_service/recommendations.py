import logging as logger

import pandas as pd


class Recommendations:
    def __init__(self) -> None:
        self._recs = {"personal": None, "default": None}
        self._stats = {"request_personal_count": 0, "request_default_count": 0}

    def load(self, type: str, path, **kwargs):
        """
        Загружаем файлы с рекомендациями
        """
        logger.info(f"Loading recommendations, type: {type}")

        self._recs[type] = pd.read_parquet(path, **kwargs)
        if type == "personal":
            self._recs[type] = self._recs[type].set_index("ncodpers")

        logger.info("Loaded {type} recommendations")

    def get_personal(self, user_id, k: int = 3):
        """
        Получаем персональные k оффлайн-рекомендаций для пользователя user_id с готовыми рекомендациями
        """
        logger.info("Get personal recommendations")

        recs = self._recs["personal"].loc[user_id]
        recs = recs["item_id"].to_list()[:k]

        self._stats["request_personal_count"] += 1
        return recs

    def get_default(self, k: int = 3):
        """
        Получаем k самых популярных items
        """
        logger.info("Get top recommendations")

        recs = self._recs["default"]
        recs = recs["item_id"].to_list()[:k]

        self._stats["request_default_count"] += 1
        return recs

    def get(self, user_id: int, k: int = 3):
        """
        Возвращаем список банковских продуктов рекомендованных данному пользователю
        """
        if user_id in self._recs["personal"].index:
            recs = self.get_personal(user_id, k=k)
        else:
            logger.info(f"There are no personal recommendations for user: {user_id}")
            recs = self.get_default(k=k)

        return recs

    def stats(self):
        logger.info("Stats for recommendations")
        for name, value in self._stats.items():
            print(f"{name:<30} {value} ")
            logger.info(f"{name:<30} {value} ")
