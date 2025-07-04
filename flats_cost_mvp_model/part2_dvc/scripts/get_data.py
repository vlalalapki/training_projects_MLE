import os

import pandas as pd
import yaml
from dotenv import load_dotenv
from sqlalchemy import create_engine


def create_connection():
    """
    Создаёт подключение к целевой PostgreSQL-базе данных, используя переменные окружения.

    Возвращает SQLAlchemy engine с параметром sslmode=require.

    Returns:
        sqlalchemy.Engine: Объект подключения к базе данных.
    """

    load_dotenv()
    host = os.environ.get("DB_DESTINATION_HOST")
    port = os.environ.get("DB_DESTINATION_PORT")
    db = os.environ.get("DB_DESTINATION_NAME")
    username = os.environ.get("DB_DESTINATION_USER")
    password = os.environ.get("DB_DESTINATION_PASSWORD")

    print("Connecting to database...")
    conn = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{db}",
        connect_args={"sslmode": "require"},
    )
    return conn


def data_to_csv():
    """
    Извлекает таблицу flats_full_clean из базы данных и сохраняет её в CSV-файл.

    Выполняет SQL-запрос к базе, читает данные в pandas DataFrame,
    и сохраняет их в файл 'data/initial_data.csv'.
    Использует индексную колонку, указанную в params.yaml.

    Returns:
        None
    """
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    conn = create_connection()
    data = pd.read_sql(
        "select * from flats_full_clean", conn, index_col=params["index_col"]
    )
    conn.dispose()

    os.makedirs("data", exist_ok=True)
    data.to_csv("data/initial_data.csv", index=None)


if __name__ == "__main__":
    data_to_csv()
