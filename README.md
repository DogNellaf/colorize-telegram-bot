# Colorize Telegram Bot

Telegram-бот для двух задач:
- раскрашивание черно-белых изображений (OpenCV DNN + Caffe-модель)
- простой диалог через OpenAI API

Реализован как проектный проект по одной из магистерских дисциплин в ходе обучения

## Разворачивание и запуск

1. Установите Python 3.9+
2. Клонируйте репозиторий и перейдите в папку проекта
3. Установите зависимости:

```bash
pip install pyTelegramBotAPI openai==0.28.0 opencv-python numpy
```

4. Скачайте файл модели `model.caffemodel` по ссылке из `models/README.md` и поместите его в папку `models/`.
5. Укажите свои ключи/токены в `bot.py`:
   - `bot = telebot.TeleBot('...')`
   - `OPENAI_API_KEY = '...'`
6. Запустите бота:

```bash
python bot.py
```

## Структура проекта

- `bot.py` — логика Telegram-бота, команды, интеграция с OpenAI.
- `colarization.py` — обработка и раскрашивание изображения через модель Caffe.
- `token_get.py` — служебный файл (сейчас пустой).
- `models/` — файлы модели (`model.prototxt`, `pts.npy`, `model.caffemodel`) и инструкция по загрузке.

## Лицензия

MIT

## Статус проекта

Проект завершен.
