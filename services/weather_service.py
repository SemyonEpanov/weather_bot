# services/weather_service.py

import aiohttp
from config import (
    ACCUWEATHER_DAILY_BASE_URL,
    ACCUWEATHER_LOCATION_URL,
    ACCUWEATHER_API_KEY
)

async def get_weather_data(location: str, days: int = 1):
    """
    Получаем прогноз погоды на 'days' дней вперёд 
    (1, 5 и т.д.) по заданному городу (location).
    Возвращаем список словарей с прогнозом или None / "api_error".
    """
    try:
        async with aiohttp.ClientSession() as session:
            # 1) Получаем location key
            params = {
                'apikey': ACCUWEATHER_API_KEY,
                'q': location
            }
            async with session.get(ACCUWEATHER_LOCATION_URL, params=params) as resp_loc:
                if resp_loc.status != 200:
                    return "api_error"
                location_data = await resp_loc.json()
                if not location_data:
                    return None
                location_key = location_data[0]['Key']

            # 2) Запрашиваем прогноз погоды на N дней
            weather_url = f"{ACCUWEATHER_DAILY_BASE_URL}/{days}day/{location_key}"
            params_weather = {
                'apikey': ACCUWEATHER_API_KEY,
                'metric': 'true',
                'details': 'true'
            }
            async with session.get(weather_url, params=params_weather) as resp_wth:
                if resp_wth.status != 200:
                    return "api_error"
                weather_data = await resp_wth.json()

            daily_forecasts = weather_data.get('DailyForecasts', [])
            if not daily_forecasts:
                return None

            # Формируем ответ
            forecasts_list = []
            for day_forecast in daily_forecasts:
                date_str = day_forecast['Date']
                temp_min = day_forecast['Temperature']['Minimum']['Value']
                temp_max = day_forecast['Temperature']['Maximum']['Value']
                day_desc = day_forecast['Day']['IconPhrase']
                day_precip = day_forecast['Day']['PrecipitationProbability']
                night_desc = day_forecast['Night']['IconPhrase']
                night_precip = day_forecast['Night']['PrecipitationProbability']

                forecasts_list.append({
                    'date': date_str,
                    'temp_min': temp_min,
                    'temp_max': temp_max,
                    'day_desc': day_desc,
                    'day_precip': day_precip,
                    'night_desc': night_desc,
                    'night_precip': night_precip
                })

            return forecasts_list

    except aiohttp.ClientError:
        return "api_error"
    except (KeyError, IndexError):
        return None
