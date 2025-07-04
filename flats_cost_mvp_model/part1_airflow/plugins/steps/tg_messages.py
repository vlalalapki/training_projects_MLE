from airflow.providers.telegram.hooks.telegram import TelegramHook


def send_telegram_success_message(context):
    """
    Отправляет сообщение в Telegram об успешном завершении DAG.

    Использует переменные окружения для получения токена бота и ID чата.
    Сообщение отправляется через TelegramHook.

    Args:
        context: Контекст выполнения DAG, содержащий ключи 'dag' и 'run_id'.

    Returns:
        None
    """
    import os

    from dotenv import load_dotenv

    load_dotenv()
    TG_TOKEN = os.getenv("TG_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    hook = TelegramHook(telegram_conn_id="test", token=TG_TOKEN, chat_id=CHAT_ID)
    dag = context["dag"]
    run_id = context["run_id"]

    message = f"Исполнение DAG {dag} с id={run_id} прошло успешно!"
    hook.send_message({"chat_id": CHAT_ID, "text": message, "parse_mode": None})


def send_telegram_failure_message(context):
    """
    Отправляет сообщение в Telegram об неудачном завершении задачи в DAG.

    Использует переменные окружения для получения токена бота и ID чата.
    Сообщение содержит run_id и идентификатор упавшей задачи.

    Args:
        context: Контекст выполнения DAG, содержащий ключи 'run_id' и 'task_instance_key_str'.

    Returns:
        None
    """
    import os

    from dotenv import load_dotenv

    load_dotenv()
    TG_TOKEN = os.getenv("TG_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    hook = TelegramHook(telegram_conn_id="test", token=TG_TOKEN, chat_id=CHAT_ID)
    task_instance_key_str = context["task_instance_key_str"]
    run_id = context["run_id"]

    message = f"Исполнение DAG с id={run_id} фэйлнулось {task_instance_key_str}"
    hook.send_message({"chat_id": CHAT_ID, "text": message, "parse_mode": None})
