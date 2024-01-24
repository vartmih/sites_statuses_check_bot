# Телеграм бот
Бот для опроса сайтов, с целью определения их работоспособности.

Бот опрашивает сайты с определенным интервалом и присылает сообщение, если сайт недоступен.
Максимальное количество отслеживаемых сайтов - 10.

## Функционал:
- Добавить сайт
- Удалить сайт
- Просмотреть весь список сайтов
- Очистить весь список сайтов
- Задать период опроса сайтов:
    - раз в 1 минуту
    - раз в 5 минут
    - раз в 10 минут
    - раз в 15 минут
    - раз в 30 минут
    - раз в 60 минут
- Запустить отслеживание статусов
- Остановить отслеживание статусов
- Просмотр персонального статуса:
  - Отслеживает сейчас бот сайты или нет
  - Количество отслеживаемых сайтов
  - Периодичность опроса


Бот запускается с помощью webhook. Для локального запуска необходимо переименовать файл .env_example
в .env и заполнить нужные переменные. 

Сам бот запускается как обычный питоновский файл:
```python
python3 src/main.py
```
