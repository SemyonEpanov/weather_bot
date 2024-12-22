# handlers/help.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    /help — отображаем помощь
    """
    await message.answer(
        "Доступные команды:\n"
        "/start — начать работу со мной\n"
        "/help — помощь\n"
        "/weather — запускает диалог для получения прогноза погоды по маршруту\n\n"
        "Команда /weather попросит указать начальную и конечную точки маршрута, "
    )
