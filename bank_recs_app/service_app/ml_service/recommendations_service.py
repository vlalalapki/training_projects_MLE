import logging
from contextlib import asynccontextmanager

import constants
from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field
from recommendations import Recommendations

fails_counter = Counter("http_request_fails_counter", "Counter of request fails")

logging.basicConfig(
    filename=constants.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("uvicorn.error")


class User(BaseModel):
    user_id: int = Field(ge=0, description="ID должен быть не отрицательный")
    k: int = Field(
        default=3,
        gt=0,
        le=9,
        description="Количество рекомендаций должно быть между 1 и 9",
    )


rec_store = Recommendations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting_now")

    rec_store.load(
        "personal",
        constants.PERSONAL_RECS_PATH,
        columns=["ncodpers", "item_id", "rang_score"],
    )

    rec_store.load(
        "default", constants.DEFAULT_RECS_PATH, columns=["item_id", "num_users"]
    )

    yield
    rec_store.stats()
    logger.info("Stopping")


app = FastAPI(title="bank_recommendations", lifespan=lifespan)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.post("/recommendations")
async def recommendations(user: User):
    """
    Получаем список рекомендованных продуктов длиной k для пользователя user_id
    """
    try:
        recs = rec_store.get(user.user_id, k=user.k)
    except KeyError:
        fails_counter.inc()

    return {"recs": recs}
