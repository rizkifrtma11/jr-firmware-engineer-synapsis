import requests
import json
import os
from datetime import datetime, timezone, timedelta

class WeatherHelper:
    def __init__(self, api_key, log_dir='log', filename='data_weather.json'):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.log_dir = log_dir
        self.filename = filename
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    

    def getTimestampGmt7(self):
        gmt7 = timezone(timedelta(hours=7))
        return datetime.now(gmt7).strftime('%Y-%m-%d %H:%M:%S')
    

    def getWeather(self, city_name):
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric'  # suhu dalam *C
        }
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                return True, {'temp': temp, 'humidity': humidity}
            else:
                return False, {'status_code': response.status_code, 'message': response.json().get('message', '')}
        except Exception as e:
            return False, {'status_code': 'Exception', 'message': str(e)}
    
    
    def saveData(self, data):
        path = os.path.join(self.log_dir, self.filename)
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Failed saving data to json: {e}")
            return False
