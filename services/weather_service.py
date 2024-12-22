# services/weather_service.py

import requests
from config import ACCUWEATHER_DAILY_BASE_URL, ACCUWEATHER_LOCATION_URL, ACC_WEATHER_API_KEY


def get_weather_data(location: str, days: int = 1):
    """
    Получаем прогноз погоды на 'days' дней вперёд 
    (1, 5 и т.д.) по заданной локации (город).
    Возвращаем список словарей, либо None / "api_error" в случае проблем.
    """
    try:
        # 1) Получаем location key
        params = {
            'apikey': ACC_WEATHER_API_KEY,
            'q': location
        }
        location_response = requests.get(ACCUWEATHER_LOCATION_URL, params=params)
        location_response.raise_for_status()
        location_data = location_response.json()
        if not location_data:
            return None
        location_key = location_data[0]['Key']

        # 2) Запрашиваем прогноз погоды на N дней
        #    Пример URL: http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}
        weather_url = f"{ACCUWEATHER_DAILY_BASE_URL}/{days}day/{location_key}"
        params = {
            'apikey': ACC_WEATHER_API_KEY,
            'metric': 'true',
            'details': 'true'
        }
        weather_response = requests.get(weather_url, params=params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        daily_forecasts = weather_data.get('DailyForecasts', [])
        if not daily_forecasts:
            return None

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

    except requests.exceptions.RequestException:
        return "api_error"
    except (KeyError, IndexError):
        return None
