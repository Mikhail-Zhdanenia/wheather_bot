import requests
import datetime
import telebot
from config import bot_token, open_wheather_token

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! я бот, который узнает погоду. Введи название города и получи прогноз на день!")


    @bot.message_handler()
    def start_message(message):

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
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_wheather_token}&units=metric")
            data = r.json()

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
            sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])  # перевод времени в удобоваримый формат
            sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) \
                                - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            string_data = f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n" \
                          f"Название города: {city}\n" \
                          f"Страна: {country}\n" \
                          f"Температура воздуха: {cur_weather}C° {wd}\n" \
                          f"Влажность: {humidity}%\n" \
                          f"Давление: {pressure} мм.рт.ст\n" \
                          f"Скорость ветра: {wind} м/с\n" \
                          f"Восход: {sunrise_time}\n" \
                          f"Закат: {sunset_time}\n" \
                          f"Продолжительность дня: {length_of_the_day}\n" \
                          f"-----Все-го хороше-го!!!-----"

            bot.send_message(message.chat.id, string_data)

        except:
            bot.send_message(message.chat.id, '\U00002620Check the City name!\U00002620')

    bot.polling()


if __name__ == '__main__':
    telegram_bot(bot_token)