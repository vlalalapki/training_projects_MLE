# Учебные проекты курса MLE

![Airflow](https://img.shields.io/badge/Airflow-191970?style=for-the-badge&logo=apacheairflow)
![Optuna](https://img.shields.io/badge/🌀%20Optuna-E0FFFF?style=for-the-badge) 
![MLflow](https://img.shields.io/badge/MLflow-f0f0f0?style=for-the-badge&logo=mlflow)
![DVC](https://img.shields.io/badge/DVC-f0f0f0?style=for-the-badge&logo=dvc)
![Docker](https://img.shields.io/badge/Docker-f0f0f0?style=for-the-badge&logo=docker)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-505050?style=for-the-badge&logo=grafana)
![Production Ready](https://img.shields.io/badge/Production_Ready-006A71?style=for-the-badge)

Этот репозиторий содержит проекты, выполненные в рамках курса **«Инженер по машинному обучению»** от [Яндекс Практикума](https://practicum.yandex.ru/machine-learning/?from=catalog) в 2024 году. В ходе работы над проектами отработаны и реализованы технологии построения и обслуживания полноценного ML-сервиса: от предобработки данных и обучения моделей до их вывода в продакшн с получением метрик и мониторингом.

---

## Ключевые навыки и изученные инструменты

- **Построение воспроизводимых ML-пайплайнов** с использованием `Airflow`, `DVC`
- **Разработка и логирование экспериментов**: отработка экспериментов, логирование параметров, артефактов в `MLflow`
- **Инженерия признаков и отбор**: `AutoFeat`, `MLxtend`
- **Подбор гиперпараметров** с помощью `Optuna` (+ MLflow)
- **Реализация REST API-сервисов** с `FastAPI` и контейнеризацией (`Docker`)
- **Мониторинг и алертинг моделей в production** автоматизация трекинга метрик с использованием `Prometheus` и `Grafana`
- **Создание рекомендательных систем**: `Implicit ALS` + CatBoost-ранжирование
- **Uplift-моделирование** с помощью `CausalML`
- **CI/CD подходы к ML-проектам**, настройка окружений, .env-конфигураций, безопасное логирование

---

## Проекты в портфолио

| 🔢 | Проект | Технологии | Описание | Особенности |
|----|--------|:--------:|---------------|----------------|
| 1️⃣ | **MVP модель: Оценка стоимости квартир**<br/>[`flats_cost_mvp_model`](flats_cost_mvp_model) | Airflow, DVC, CatBoost, scikit-learn, Telegram API | Построение базового ML-пайплайна на Airflow + DVC для обработки данных и обучения модели в контексте предсказания стоимости недвижимости |  Основное внимание на грамотное построение DAG для airflow и dvc-пайплайна |
| 2️⃣ | **Улучшение baseline-модели**<br/>[`flats_cost_model_improvement`](flats_cost_model_improvement) | MLflow, AutoFeat, MLxtend, Optuna, CatBoost | Улучшение ML модели за счёт расширенной генерации признаков, отбора фичей и автоматического подбора гиперпараметров | Основное внимание на feature engineering, feature selection, настройка и логирование в mlflow |
| 3️⃣ | **Вывод модели в production**<br/>[`flats_cost_app`](flats_cost_app) | FastAPI, Docker, Prometheus, Grafana | Создание REST API-сервиса для инференса ML модели и мониторинга её работы | Основное внимание на работу с FastAPI, сборку docker-контейнеров и настройку их совместной работы |
| 4️⃣ | **Рекомендательная система для банка**<br/>[`bank_recs_app`](bank_recs_app) | Implicit ALS, CatBoost, MLflow, FastAPI, Prometheus, Grafana, Docker | Гибридная система рекомендаций банковских продуктов + REST API-сервис для получения готовых рекомендаций | Основное внимание на отработку навыков работы с изученными технологиями + базовая работа с рекомендациями |

---


> Каждый проект имеет собственный `README.md` с инструкциями и описанием.

---