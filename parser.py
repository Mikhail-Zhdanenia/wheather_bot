import requests
import datetime
from pprint import pprint
from config import open_wheather_token


def get_weather(city, open_wheather_token):

    code_to_smile = {
        "Clear": "ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "мелкий дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_wheather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Сорентируйся по местным условиям, визуально'

        humidity = data['main']["humidity"]
        pressure = data['main']["pressure"]
        wind = data['wind']['speed']
        country = data['sys']['country']
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) #перевод времени в удобоваримый формат
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Название города: {city}\n"
              f"Страна: {country}\n"
              f"Температура воздуха: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\n"
              f"Давление: {pressure} мм.рт.ст\n"
              f"Скорость ветра: {wind} м/с\n"
              f"Восход: {sunrise_time}\n"
              f"Закат: {sunset_time}\n"
              f"Продолжительность дня: {length_of_the_day}")


    except Exception as ex:
        print(ex)
        print('Check the City name!')


def main():
    city = input("Enter the name of city: ")
    get_weather(city, open_wheather_token)


if __name__=='__main__':
    main()