# Habit Tracker API

Этот проект представляет собой backend-сервис для трекинга полезных привычек с интеграцией Telegram и асинхронными задачами через Celery.

## 🚀 Возможности

- Регистрация и авторизация пользователей через JWT.
- CRUD-интерфейс для привычек.
- Уведомления через Telegram-бота.
- Асинхронные задачи (отправка сообщений) через Celery и Redis.
- Поддержка периодических задач через celery-beat.
- Документация API через drf-spectacular.
- Покрытие тестами с использованием Django TestCase и APITestCase.

## 🧱 Стек технологий

- Python 3.12
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis
- Celery + celery-beat
- drf-spectacular
- httpx (для Telegram API)
- coverage (для анализа покрытия кода)
- Poetry (для управления зависимостями)

## 🛠️ Установка

```bash
git clone https://github.com/your-username/course_work_5.git
cd course_work_5
poetry install
cp .env.example .env  # создайте свой .env с переменными окружения
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## 📋 Основные команды

```bash
# Тестирование
poetry run python manage.py test

# Покрытие кода
poetry run coverage run --source='.' manage.py test
poetry run coverage html
poetry run coverage report

# Celery
poetry run celery -A config worker --loglevel=info
poetry run celery -A config beat --loglevel=info
```

## 📎 Переменные окружения

В файле `.env` необходимо указать:

```
DATABASE_URL=postgres://user:password@localhost:5432/db_name
SECRET_KEY=your_secret_key
DEBUG=True
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 📄 Документация

Swagger UI доступен по адресу:
```
/api/docs/
```

## 🧪 Тестирование

Проект покрыт тестами:
- `users/tests.py`
- `habits/tests.py`

Покрытие проверено с помощью `coverage`.