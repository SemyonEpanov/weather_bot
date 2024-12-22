# handlers/weather.py

from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from states.weather_states import WeatherStates
from services.weather_service import get_weather_data

router = Router()

@router.message(Command("weather"))
async def cmd_weather(message: Message, state: FSMContext):
    """
    /weather — начинаем пошаговый диалог: просим указать начальную точку.
    """
    await state.set_state(WeatherStates.waiting_for_start_location)
    await message.answer("Введите вашу начальную точку (город):")


@router.message(WeatherStates.waiting_for_start_location)
async def process_start_location(message: Message, state: FSMContext):
    """
    Сохраняем стартовую локацию, переходим к запросу конечной точки.
    """
    start_location = message.text.strip()
    await state.update_data(start_location=start_location)

    await state.set_state(WeatherStates.waiting_for_end_location)
    await message.answer("Отлично! Теперь введите конечную точку (город):")


@router.message(WeatherStates.waiting_for_end_location)
async def process_end_location(message: Message, state: FSMContext):
    """
    Сохраняем конечную локацию, спрашиваем про промежуточные.
    """
    end_location = message.text.strip()
    await state.update_data(end_location=end_location)

    # Переходим к запросу промежуточных точек.
    await state.set_state(WeatherStates.waiting_for_intermediate_locations)
    await message.answer(
        "Есть ли у вас промежуточные остановки?\n"
        "Если да, перечислите их через запятую.\n"
        "Если нет, просто напишите 'нет'."
    )


@router.message(WeatherStates.waiting_for_intermediate_locations)
async def process_intermediate_locations(message: Message, state: FSMContext):
    text = message.text.strip().lower()

    if text == "нет":
        intermediate_locations = []
    else:
        intermediate_locations = [loc.strip() for loc in message.text.split(",") if loc.strip()]

    await state.update_data(intermediate_locations=intermediate_locations)

    # Переходим к выбору "сколько дней вперёд" хотим прогноз
    await state.set_state(WeatherStates.waiting_for_days_choice)

    # Делаем inline-клавиатуру с выбором
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день", callback_data="days_1")],
        [InlineKeyboardButton(text="3 дня", callback_data="days_3")],
        [InlineKeyboardButton(text="5 дней", callback_data="days_5")]
    ])
    await message.answer("Выберите, на сколько дней вперёд вы хотите прогноз:", reply_markup=keyboard)


@router.callback_query(WeatherStates.waiting_for_days_choice, Text(startswith="days_"))
async def process_days_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатываем нажатие кнопки с выбором количества дней.
    """
    days_str = callback.data.split("_")[1]
    days = int(days_str)  # например, 1, 3, 5
    await state.update_data(days=days)

    data = await state.get_data()
    start = data['start_location']
    end = data['end_location']
    interm = data['intermediate_locations']

    route_info = (
        f"Маршрут:\n\nНачало: {start}\n"
        + (f"Промежуточные: {', '.join(interm)}\n" if interm else "")
        + f"Конец: {end}\n\n"
        f"Прогноз на {days} {'день' if days == 1 else 'дней'}."
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="confirm_route"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel_route")
        ]
    ])
    await callback.message.edit_text(route_info, reply_markup=keyboard)
    await state.set_state(WeatherStates.confirm_route)
    await callback.answer()


@router.callback_query(WeatherStates.confirm_route, Text("cancel_route"))
async def process_cancel_route(callback: CallbackQuery, state: FSMContext):
    """Отмена запроса прогноза."""
    await callback.message.edit_text("Запрос прогноза отменён. Для нового запроса используйте /weather.")
    await state.clear()
    await callback.answer()


@router.callback_query(WeatherStates.confirm_route, Text("confirm_route"))
async def process_confirm_route(callback: CallbackQuery, state: FSMContext):
    """
    Подтверждаем маршрут и показываем результат.
    """
    await callback.answer("Пожалуйста, подождите, запрашиваю прогноз погоды...")

    data = await state.get_data()
    days = data['days']
    locations = [data['start_location']] + data['intermediate_locations'] + [data['end_location']]

    result_text_parts = []

    for i, loc in enumerate(locations, start=1):
        # Вызов асинхронной функции получения погоды
        forecasts_list = await get_weather_data(loc, days)
        if forecasts_list == "api_error":
            part = f"Город: {loc}\nНе удалось связаться с API AccuWeather. Попробуйте позже."
        elif forecasts_list is None:
            part = f"Город: {loc}\nНе удалось получить данные. Возможно, указан неверный город?"
        else:
            part_header = f"**{i}. {loc}**\n"
            lines = []
            for day_data in forecasts_list:
                lines.append(
                    f"Дата: {day_data['date']}\n"
                    f"  Темп. мин: {day_data['temp_min']}°C, макс: {day_data['temp_max']}°C\n"
                    f"  Днём: {day_data['day_desc']} (вер. осадков {day_data['day_precip']}%)\n"
                    f"  Ночью: {day_data['night_desc']} (вер. осадков {day_data['night_precip']}%)\n"
                )
            part = part_header + "\n".join(lines)
        result_text_parts.append(part)

    result_text = "\n---\n".join(result_text_parts)

    await callback.message.edit_text(result_text)
    await state.clear()
