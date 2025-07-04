import pendulum
from airflow.decorators import dag, task
from steps.clean_data import output, remove_duplicates
from steps.tg_messages import (
    send_telegram_failure_message,
    send_telegram_success_message,
)


@dag(
    schedule="@once",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    tags=["ETL", "Clean"],
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
)
def clean_flats_dataset():
    """
    DAG для очистки датасета с квартирами: удаление дубликатов и выбросов.

    Этапы:
    - Создание таблицы flats_full_clean, если она отсутствует.
    - Извлечение данных из таблицы flats_full.
    - Очистка данных: удаление дубликатов и выбросов.
    - Загрузка очищенных данных в таблицу flats_full_clean.

    DAG выполняется один раз и отправляет уведомления в Telegram при успехе/ошибке.
    """
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    @task()
    def create_clean_table():
        """
        Создаёт таблицу flats_full_clean в базе данных, если она ещё не существует.

        Таблица содержит очищенные данные о квартирах, без столбца 'studio',
        и с уникальным ограничением по полю 'id'.

        Returns:
            None
        """
        from sqlalchemy import (
            BigInteger,
            Column,
            Float,
            MetaData,
            Numeric,
            String,
            Table,
            UniqueConstraint,
            inspect,
        )

        hook = PostgresHook("my_bd")
        conn_bd = hook.get_sqlalchemy_engine()
        metadata = MetaData()
        flats_clean_name = Table(
            "flats_full_clean",
            metadata,
            Column("id", BigInteger, primary_key=True, autoincrement=True),
            Column("floor", BigInteger),
            Column("is_apartment", String),
            Column("kitchen_area", Float),
            Column("living_area", Float),
            Column("rooms", BigInteger),
            Column("total_area", Float),
            Column("target", Numeric),
            Column("build_year", BigInteger),
            Column("building_type_int", BigInteger),
            Column("latitude", Float),
            Column("longitude", Float),
            Column("ceiling_height", Float),
            Column("flats_count", BigInteger),
            Column("floors_total", BigInteger),
            Column("has_elevator", String),
            UniqueConstraint("id", name="unique_cl_flats_constraint"),
        )
        if not inspect(conn_bd).has_table("flats_full_clean"):
            metadata.create_all(conn_bd)
        pass

    @task()
    def extract():
        """
        Извлекает все данные из таблицы flats_full в базе данных.

        Использует подключение к PostgreSQL через Airflow PostgresHook.

        Returns:
            DataFrame: Извлечённые данные.
        """
        hook = PostgresHook("my_bd")
        conn = hook.get_conn()
        sql = """
        SELECT *
        FROM flats_full
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        """
        Очищает данные: удаляет дубликаты строк и выбросы.

        Использует функции `remove_duplicates` и `output` из модуля clean_data.

        Args:
            data: DataFrame, полученный из таблицы flats_full.

        Returns:
            DataFrame: Очищенные данные, готовые к загрузке.
        """
        data = remove_duplicates(data)
        data = output(data)

        return data

    @task()
    def load(data: pd.DataFrame):
        """
        Загружает очищенные данные в таблицу flats_full_clean в базу данных PostgreSQL.

        Использует метод insert_rows с параметром replace=True для замены строк
        по значению поля 'id'.

        Args:
            data: Очищенный DataFrame, полученный на предыдущем шаге.

        Returns:
            None
        """
        hook = PostgresHook("my_bd")
        hook.insert_rows(
            table="flats_full_clean",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=["id"],
            rows=data.values.tolist(),
        )

    create_clean_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)


clean_flats_dataset()
