# states/weather_states.py
from aiogram.fsm.state import State, StatesGroup

class WeatherStates(StatesGroup):
    waiting_for_start_location = State()
    waiting_for_end_location = State()
    waiting_for_intermediate_locations = State()
    waiting_for_days_choice = State()
    confirm_route = State()
    show_result = State()
