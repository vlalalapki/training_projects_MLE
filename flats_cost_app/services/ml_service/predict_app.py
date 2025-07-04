"""FastAPI-приложение для модели предсказания стоимости квартиры."""

from fastapi import Body, FastAPI
from handler import FastApiHandler
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.handler = FastApiHandler()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

app_predictions = Histogram(
    "app_predictions",
    "Histogram of model predictions",
    buckets=(2e6, 4e6, 7e6, 14e6, 25e6, 1e10),
)

fails_counter = Counter("http_request_fails_counter", "Counter of request fails")


@app.get("/")
def read_root():
    return {"Hello": "Use .../docs"}


@app.post("/api/cost/")
def get_predictions_for_object(
    object_id: str,
    model_params: dict = Body(
        example={
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
    ),
):
    """Функция для получения стоимости квартиры.

    Args:
        object_id (str): Идентификатор объекта недвижимости.
        model_params (dict): Параметры объекта недвижимости, которые нужно передать в модель.

    Returns:
        dict: Предсказание, стоимость объекта недвижимости.
    """
    all_params = {"object_id": object_id, "model_params": model_params}

    response = app.handler.handle(all_params)

    try:
        response["object_cost"]
        app_predictions.observe(response["object_cost"][0])
    except KeyError:
        fails_counter.inc()

    return response
