# Методичка 11 потока

Короткий маршрут повторения первой части модуля «Python. Алгоритмические задачи и Telegram-боты» по темам и проектам 11 потока.

## Локальный запуск

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

Сайт откроется по адресу `http://127.0.0.1:8000`.

## Проверка и публикация

```bash
mkdocs build --strict
```

Каждый push в ветку `main` запускает GitHub Actions и публикует собранный сайт в GitHub Pages.
