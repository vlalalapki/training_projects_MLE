# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории с проектом

## 1. FastAPI микросервис в виртуальном окружение

Для запуска микросервиса в виртуальном окружении, необходимо установить само окружение и его зависимости из файла requirements.txt

```bash
#установка виртуального окружения 
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_project_name

#активация окружения и уствновка зависимостей
source .venv_project_name/bin/activate
pip install -r requirements.txt
```
Далее необходимо перейти в директорию services/ml_service и запустить приложение с помощью uvicorn
```bash
# команда перехода в директорию
cd services/ml_service

# команда запуска сервиса
uvicorn predict_app:app --reload --port 1702 --host 0.0.0.0

```
### Пример curl-запроса к микросервису

```bash
#легкий запрос - проверка работоспособности приложения
curl "http://localhost:1702/"

#полный пример запрос на предсказание цены квартиры
curl -X 'POST' \
  'http://localhost:1702/api/cost/?object_id=332' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
  "longitude": 29
}'
```
## 2. FastAPI микросервис в Docker-контейнере
Для запуска микросервиса в одном Docker-контейнере необходимо перейти в директорию services и запустить построение контейнера из Dockerfile
```bash
# команда перехода в нужную директорию
cd services
# команды для запуска микросервиса в режиме docker container
docker image build . --tag app:predict
docker container run --publish 1702:1702 --volume=./models:/services/models --env-file .env app:predict
```
### Пример curl-запроса к микросервису
```bash
#легкий запрос - проверка работоспособности приложения
curl "http://localhost:1702/"

#полный пример запрос на предсказание цены квартиры

curl -X 'POST' \
  'http://localhost:1702/api/cost/?object_id=3323' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
  "longitude": 29
}'
```

## 3. Docker compose для микросервиса и системы моониторинга
Для запуска сервисов необходимо перейти в директорию services и запустить построение Docker compose из файла docker-compose.yaml
```bash
# команда перехода в нужную директорию
cd services

# команды для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису

```bash
#легкий запрос - проверка работоспособности приложения
curl "http://localhost:1702/"

#полный пример запрос на предсказание цены квартиры

curl -X 'POST' \
  'http://localhost:1702/api/cost/?object_id=3323' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
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
  "longitude": 29
}'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 30 запросов к модели в приложении в течение около 5 минут. На 15м запросе остановка на 20 секунд. Часть запросов имеет некорректные параметры ввода, это сделано для проверки метрики, считающей ошибочные запросы.
Команды необходимые для запуска скрипта:

```bash
# команда перехода в нужную директорию
cd services

# команды для запуска скрипта
python3.10 fake_queries.py

```

Адреса сервисов:
- микросервис: http://localhost:1702
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000