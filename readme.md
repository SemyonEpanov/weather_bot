# Weather Bot

> **Telegram-бот для получения прогноза погоды** на несколько дней вперёд с поддержкой маршрутов: начальная точка, промежуточные остановки и конечная.

---

## Возможности

- **Прогноз погоды** для заданных точек маршрута:
  - Начальная точка
  - Промежуточные точки (неограниченное количество)
  - Конечная точка

### Основные команды
| Команда    | Описание                                                                                     |
|------------|----------------------------------------------------------------------------------------------|
| `/start`   | Приветствие и краткое описание возможностей бота                                             |
| `/help`    | Список доступных команд и краткая инструкция                                                 |
| `/weather` | Запуск пошагового сценария (FSM): ввод начальной/конечной точек, промежуточных остановок и т.д. |

---

## Технологии

- [**Requests**](https://docs.python-requests.org/)
- [**Aiogram v3**](https://docs.aiogram.dev/en/dev-3.x/) — фреймворк для написания Telegram-ботов  
- [**AccuWeather API**](https://developer.accuweather.com/) — сервис для получения прогноза погоды

---

## Структура проекта

```bash
my_weather_bot/
├── config.py                  # Настройки (токен бота, ключ к API и пр.)
├── services/
│   ├── __init__.py
│   └── weather_service.py     # Логика запроса к AccuWeather API
├── states/
│   ├── __init__.py
│   └── weather_states.py      # Определения FSM-состояний бота
├── handlers/
│   ├── __init__.py
│   ├── start.py               # Обработчик команды /start
│   ├── help.py                # Обработчик команды /help
│   └── weather.py             # Обработка /weather, FSM, инлайн-кнопки
├── main.py                    # Точка входа. Запускает бота (dp.run_polling)
└── requirements.txt           # Зависимости проекта (aiogram, requests и т.д.)
```

---

## Запуск

- **Шаги** для запуска проекта:
  - Клонируем репозиторий
  - Устанавливаем необходимые пакеты
  - Ставим API-keys в config.py
  - Запускаем + радуемся

```bash
git clone https://github.com/SemyonEpanov/weather_bot.git
cd weather_bot
```

```bash
pip install -r requirements.txt
```

```bash
TELEGRAM_BOT_TOKEN = ""
ACCUWEATHER_API_KEY = ""
```

```bash
python main.py
```
---