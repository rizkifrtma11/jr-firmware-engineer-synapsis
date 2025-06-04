from function.weather_helper import WeatherHelper
import time

def inputInterval():
    while True:
        user_input = input("Masukkan interval sampling (detik, angka > 0): ").strip()
        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        else:
            print("Input salah! Harap masukkan angka lebih besar dari 0.")


def main():
    API_KEY = '7a1af3f979ec4fe99ac43e3f07abed0e'
    city_name = input("Masukkan nama kota: ").strip()
    interval = inputInterval()

    weather = WeatherHelper(API_KEY)

    while True:
        success, result = weather.getWeather(city_name)
        timestamp = weather.getTimestampGmt7()
        if success:
            weather.saveData(result)
            print(f"{timestamp} - Success Running Sampling Data Weather with Result Temperature {result['temp']} °C & Humidity {result['humidity']} %")
        else:
            print(f"{timestamp} - Failed Running Sampling Data Weather with Status Code {result['status_code']} - {result['message']}")
        
        time.sleep(interval)


if __name__ == "__main__":
    main()
