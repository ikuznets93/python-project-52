# Менеджер задач (Python)

[![hexlet-check](https://github.com/ikuznets93/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ikuznets93/python-project-52/actions)

На практике узнаете о проектировании баз данных, PaaS, мониторинге ошибок, ORM, фреймворке Django, шаблонизации и Tailwind CSS.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python
Как это должно работать: https://files.hexlet.app/a/0rkpse

## Стек

- Python

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

## Развёртывание на Railway

Проект подготовлен к Railway: Railpack определит Python и `uv`, установит
зависимости, а `railpack.json` задаёт команду запуска — сборка статики,
миграции и gunicorn.

1. Запушьте репозиторий на GitHub.
2. В [Railway](https://railway.com) создайте проект:
   **New Project → Deploy from GitHub repo** и выберите репозиторий.
3. Добавьте базу: **New → Database → PostgreSQL**.
4. В сервисе приложения откройте **Variables** и добавьте:
   - `SECRET_KEY` — случайная строка:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(64))"
     ```
   - `DEBUG=False`;
   - `DATABASE_URL=${{Postgres.DATABASE_URL}}` — если сервис базы называется
     иначе, подставьте его имя.
5. Нажмите **Deploy**. При старте контейнера выполняются:
   - `collectstatic`;
   - `migrate`;
   - запуск gunicorn на `$PORT`.
6. Railway автоматически добавляет домен `*.up.railway.app` в `ALLOWED_HOSTS`
   и `CSRF_TRUSTED_ORIGINS` через `RAILWAY_PUBLIC_DOMAIN`. Для своего домена
   задайте переменные вручную:
   ```env
   ALLOWED_HOSTS=example.com,www.example.com
   CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
   ```
7. Суперпользователь создаётся через Railway CLI:
   ```bash
   railway link
   railway ssh
   python manage.py createsuperuser
   ```

Статику раздаёт WhiteNoise. При необходимости healthcheck можно указать в
настройках сервиса: **Settings → Healthcheck → Path = `/`**.

## Развёртывание на Render

В репозитории есть `render.yaml` — [Blueprint](https://render.com/docs/infrastructure-as-code),
который создаёт веб-сервис и PostgreSQL:

1. Запушьте репозиторий на GitHub.
2. В [Render Dashboard](https://dashboard.render.com) выберите **New → Blueprint** и подключите репозиторий.
3. Нажмите **Apply** и дождитесь окончания сборки.

Render автоматически настраивает окружение:

- `SECRET_KEY` генерируется Render;
- `DEBUG=False`;
- `DATABASE_URL` берётся из созданной базы;
- `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` подставляются из `RENDER_EXTERNAL_HOSTNAME` и `RENDER_EXTERNAL_URL`.

При сборке выполняется `collectstatic`, при старте — миграции и gunicorn.
Статику раздаёт WhiteNoise.

### Ограничения бесплатного плана

- Веб-сервис засыпает после 15 минут без запросов; первый запрос после сна занимает около минуты.
- PostgreSQL бесплатного плана живёт 30 дней, после чего его нужно перевести на платный план.
- Исходящие SMTP-порты (25/465/587) закрыты — для отправки писем нужен внешний API или платный план.
- Shell на free-плане недоступен. Суперпользователя можно создать локально, подключившись к внешнему URL базы:
  ```bash
  DATABASE_URL='<external database url>' uv run python manage.py createsuperuser
  ```

## Использование

<!-- Добавьте примеры запуска и запись asciinema — именно это смотрит работодатель -->

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
