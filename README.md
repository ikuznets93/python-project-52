# Менеджер задач (Python)

[![hexlet-check](https://github.com/ikuznets93/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ikuznets93/python-project-52/actions)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ikuznets93_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ikuznets93_python-project-52)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ikuznets93_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ikuznets93_python-project-52)

На практике узнаете о проектировании баз данных, PaaS, мониторинге ошибок, ORM, фреймворке Django, шаблонизации и Tailwind CSS.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python
Как это должно работать: https://files.hexlet.app/a/0rkpse

## Демонстрация

https://python-project-52-production.up.railway.app/ (Последние два 2 дня деплой на railway приостановлен)

## Стек

- Python
- Django
- HTML/CSS
- Tailwind
- PostgreSQL
- Rollbar (Error Tracking)

## Установка

```bash
git clone https://github.com/ikuznets93/python-project-52.git
cd python-project-52
uv sync
cp .env.example .env
```

В `.env` укажите `SECRET_KEY` и при необходимости остальные переменные. Локально
можно оставить `DATABASE_URL` пустым — тогда используется SQLite.

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

### Сборка CSS

Если менялись шаблоны или Tailwind-классы, пересоберите стили:

```bash
uv run python manage.py tailwind build --force
```

Собранный `assets/css/tailwind.css` хранится в репозитории и попадает в `staticfiles` при `collectstatic`.

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
