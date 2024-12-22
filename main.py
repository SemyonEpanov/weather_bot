# main.py
import logging
from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN
from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.weather import router as weather_router

def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="Markdown")
    dp = Dispatcher()

    # Регистрируем все роутеры
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(weather_router)

    # Запуск бота (поллинг)
    dp.run_polling(bot)

if __name__ == "__main__":
    main()
