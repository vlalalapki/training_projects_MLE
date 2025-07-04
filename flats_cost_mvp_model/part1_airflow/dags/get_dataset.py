import pendulum
from airflow.decorators import dag, task
from steps.tg_messages import (
    send_telegram_failure_message,
    send_telegram_success_message,
)


@dag(
    schedule="@once",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ETL"],
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
)
def prepare_flats_dataset():
    """
    DAG для извлечения, преобразования и загрузки данных о квартирах из PostgreSQL.

    Этапы:
    - Создание таблицы flats_full, если она отсутствует.
    - Извлечение данных из таблиц flats и buildings.
    - Преобразование данных (переименование столбца price в target).
    - Загрузка преобразованных данных в таблицу flats_full с заменой по id.

    DAG выполняется один раз и отправляет уведомления в Telegram по завершении.
    """
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    @task()
    def create_table():
        """
        Создаёт таблицу flats_full в базе данных, если она ещё не существует.

        Таблица содержит информацию о квартирах, включая характеристики
        недвижимости и местоположение. Создание выполняется через SQLAlchemy.

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
        flats_full_name = Table(
            "flats_full",
            metadata,
            Column("id", BigInteger, primary_key=True, autoincrement=True),
            Column("floor", BigInteger),
            Column("is_apartment", String),
            Column("kitchen_area", Float),
            Column("living_area", Float),
            Column("rooms", BigInteger),
            Column("studio", String),
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
            UniqueConstraint("id", name="unique_flats_constraint"),
        )
        if not inspect(conn_bd).has_table("flats_full"):
            metadata.create_all(conn_bd)
        pass

    @task()
    def extract(**kwargs):
        """
        Извлекает данные о квартирах и связанных зданиях из таблиц PostgreSQL.

        Выполняется SQL-запрос с объединением таблиц flats и buildings.
        Результат содержит характеристики квартиры и здания.

        Returns:
            DataFrame: Извлечённые данные в формате pandas.
        """

        hook = PostgresHook("my_bd")
        conn = hook.get_conn()
        sql = """
        select
            fl.id, fl.floor, fl.is_apartment, fl.kitchen_area, fl.living_area, fl.rooms,
            fl.studio, fl.total_area, fl.price, bld.build_year, bld.building_type_int,
            bld.latitude, bld.longitude, bld.ceiling_height, bld.flats_count,
            bld.floors_total, bld.has_elevator
        from flats as fl 
        left join buildings as bld on bld.id = fl.building_id
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        """
        Преобразует извлечённые данные, переименовывая колонку 'price' в 'target'.

        Args:
            data: DataFrame, полученный из предыдущего шага extract.

        Returns:
            DataFrame: Преобразованные данные.
        """
        data = data.rename(columns={"price": "target"})
        return data

    @task()
    def load(data: pd.DataFrame):
        """
        Загружает преобразованные данные в таблицу flats_full в базе данных PostgreSQL.

        Использует метод insert_rows с параметром replace=True для замены
        существующих строк по первичному ключу 'id'.

        Args:
            data: DataFrame, полученный из этапа transform.

        Returns:
            None
        """
        hook = PostgresHook("my_bd")
        hook.insert_rows(
            table="flats_full",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=["id"],
            rows=data.values.tolist(),
        )

    create_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)


prepare_flats_dataset()
