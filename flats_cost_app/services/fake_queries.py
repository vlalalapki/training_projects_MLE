import random
import time

import numpy as np
import requests

# отправляем на сервис запросы
for i in range(30):
    object_id = "666"
    params = {
        "floor": random.randint(1, 35),
        "is_apartment": random.choice([0, 1]),
        "kitchen_area": random.randint(4, 30),
        "total_area": random.randint(25, 200),
        "build_year": random.randint(1910, 2000),
        "building_type_int": random.randint(1, 7),
        "ceiling_height": np.round(random.uniform(2.5, 5), 2),
        "flats_count": random.randint(10, 2000),
        "floors_total": random.randint(1, 35),
        "has_elevator": random.choice([0, 1]),
        "latitude": np.round(random.uniform(33, 40), 2),
        "longitude": np.round(random.uniform(25, 36), 2),
    }

    if i in [2, 8, 11, 15]:
        params.update({"total_area": ""})

    response = requests.post(
        "http://localhost:1702/api/cost/?object_id=666",
        json=params,
    )

    print(response.json())
    # на 15м запросе перерыв 20 секунд
    if i == 15:
        time.sleep(20)

    # после каждого запроса перерыв 7 секунд
    time.sleep(7)
