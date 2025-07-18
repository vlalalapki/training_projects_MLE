# Создание системы рекомендаций для банковских продуктов

## Описание проекта

В данном проекте мы проводим исследование имеющихся банковских данных и создаем систему рекомендаций банковских продуктов различным группам клиентов.

Основной целью будет приобретение клиентом большего количества банковских продуктов (кредиты, депозиты, инвестиционные продукты).

Система рекомендации строится на разделении пользователей на 2 основные группы:
- холодные пользователи - клиенты банка не имеющие ни одного банковского продукта. Для них сервис предлагает самые популярные банковские продукты.
- пользователи с историей - те, кто уже пользуются банковскими продуктами. Для таких пользователей мы строим рекомендации на основе матричной факторизации (implicit.ALS). Затем добавляем к данным характеристики самого пользователя, дополнительные сгенерированные признаки и подаем все в модель для ранжирования. На выходе получаем персональные рекомендации для пользователя на следующий календарный месяц.

Реализован FastAPI-сервис, предоставляющий REST API для получения готовых рекомендаций по банковским продуктам. Сервис контейнеризирован с помощью Docker и сопровождается системой мониторинга на базе Prometheus и Grafana.

---

## Используемые технологии

- FastAPI, Uvicorn;
- Docker, Docker Compose;
- Prometheus;
- Grafana;
- основные библиотеки для работы с проектом:
    * prometheus_client, prometheus_fastapi_instrumentator;
    * Scikit-learn;
    * Implicit;
    * CatBoost;
    * Pandas;
    * numpy.

--- 

## Конфигурация проекта

```
bank_recs_app/
├── artifacts/              
│   ├── EDA/                              <- Артефакты со стадии EDA. 
│   ├── models/                           <- Артефакты со стадии разработки моделями. 
│ 
├── data/  
│   ├── processed/                        <- Преобразованные данные для моделей. 
│   ├── raw/                              <- Оригинальные, сырые данные. 
│   └── recs/                             <- Файлы с промежуточными рекомендациями. 
│ 
├── mlflow_server/                        <- файлы для запуска mlflow_server. 
│ 
├── research_and_notebooks/               <- Jupyter notebooks для разработки моделей и рекомендаций. 
│ 
├── service_app/                          <- Компоненты приложения для рекомендаций. 
│   ├── ml_service/                       <- Часть, отвечающая за сервис рекомендаций. 
│   │   ├── constants.py                  <- Файл с константами. 
│   │   ├── recommendations_service.py    <- Файл с сервисом FastAPI. 
│   │   └── recommendations.py            <- Файл с классом-обработчиком. 
│   │ 
│   ├── prometheus/                       <- Настройки работы сервиса prometheus. 
│   ├── recs/                             <- Файлы с готовыми рекомендациями.                  
│   ├── .env                              <- Креды и порты для компонентов приложения. 
│   ├── docker-compose.yaml               <- Конфигурация сборки в докере всех сервисов. 
│   ├── Dockerfile                        <- Конфигурация сборки в докере сервиса с рекомендациями. 
│   └── requirements.txt                  <- Зависимости для сборки докера 
│
├── .env                                  <- Переменные окружения
├── .gitignore                            <- Исключения для git
├── README.md                             <- Описание проекта и работы с ним.  
└── requirements.txt                      <- Зависимости для сборки проекта 
```


## Инструкции по работе с проектом

Склонируйте репозиторий проекта:

```bash
git clone https://github.com/vlalalapki/training_projects_MLE
cd training_projects_MLE/bank_recs_app
```

### Запуск в виртуальном окружении
Для запуска микросервиса в виртуальном окружении, необходимо установить само окружение и его зависимости из файла requirements.txt

```bash
#установка виртуального окружения 
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_project_name

#активация окружения и установка зависимостей
source .venv_project_name/bin/activate
pip install -r requirements.txt
```
Далее необходимо перейти в директорию service_app/ml_service и запустить приложение с помощью uvicorn
```bash
# команда перехода в директорию
cd service_app/ml_service

# команда запуска сервиса
uvicorn recommendations_service:app --reload --port 1702 --host 0.0.0.0

```

### Запуск в Docker compose для микросервиса и системы мониторинга
Для запуска сервисов необходимо перейти в директорию service_app и запустить построение Docker compose из файла docker-compose.yaml

```bash
# команда перехода в нужную директорию
cd service_app

# команды для запуска микросервиса в режиме docker compose
docker compose up --build
```