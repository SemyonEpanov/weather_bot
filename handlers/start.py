# handlers/start.py
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start — приветствие и краткое описание возможностей
    """
    await message.answer(
        "Привет! Я бот-прогноз погоды.\n"
        "Я могу показать прогноз погоды на несколько дней вперёд для вашего маршрута.\n"
        "Введите /help, чтобы узнать, как мной пользоваться."
    )
