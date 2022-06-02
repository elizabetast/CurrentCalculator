import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import requests
import json
from datetime import datetime

from config import bot, APPID, keys
from exceptions import ConvertionExeption
from utils import get_wind_direction, get_exchange_rate
from texts import KeyboardTexts


@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                 row_width=2)
    weather_button = KeyboardButton(KeyboardTexts.WEATHER)
    currency_rate_button = KeyboardButton(KeyboardTexts.CURRENCY_RATE)
    exchange_currency_button = KeyboardButton(KeyboardTexts.EXCHANGE_CURRENCY)
    markup.add(weather_button, currency_rate_button, exchange_currency_button)
    bot.send_message(message.chat.id,
                     f"Привет, {message.chat.username}."
                     f"\nВыберите действие.",
                     reply_markup=markup)


def request_forecast(message):
    """Function showing weather forecast for a day.

    :arg message: request from bot.

    :return: message with forecast data.

    """
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': 519690, 'units': 'metric',
                                   'lang': 'ru', 'APPID': APPID})
        data = res.json()
        today = datetime.now().day
        today_forecast = list(
            filter(lambda x: datetime.strptime(x["dt_txt"][:10], "%Y-%m-%d").day == today, data['list']))
        result = ["🌥 Погода на сегодня\n"]
        for i in today_forecast:
            time = datetime.strptime(i["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            result.append(
                f"⏰ {time}:\n🌡 {i['main']['temp']} °C\n💨 {str(i['wind']['speed'])}м/с. {i['weather'][0]['description']} Направление: {get_wind_direction(i['wind']['deg'])}\n")

        bot.send_message(message.chat.id, "\n".join(result))
    except Exception as e:
        bot.reply_to(message, f'Погода не найдена.\n{e}')


def converter(message: telebot.types.Message):
    """Money exchange function.

    :arg message: request from bot.

    :return: message with amount exchanged.

    """
    try:
        values = message.text.split()  # проверка что введено три параметра

        if len(values) != 3:
            raise ConvertionExeption('Слишком много параметров.')

        quote, base, amount = values
        if quote == base:
            raise ConvertionExeption(
                f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote.upper()]  # RUB

        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base.upper()]  # EUR
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)  # 1000
        except ValueError:
            raise ConvertionExeption(
                f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey=d84cf1bb0ece1d1a78a5')
        total_base = json.loads(r.content)
        total_base = total_base[f"{quote}_{base}"]
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {quote} = {round(float(total_base), 3) * amount} {base} '  # вывод подсчётов
        bot.send_message(message.chat.id, text)


def request_available_currency(message: telebot.types.Message):
    """Function showing list of available currency.

    :arg message: request from bot.

    :return: message list of currency.

    """
    bot.send_message(message.chat.id, f'Доступные валюты: \n' \
                                      f'USD = {get_exchange_rate("usd")} RUB \n' \
                                      f'EUR = {get_exchange_rate("eur")} RUB')


def exchange_currency(message: telebot.types.Message):
    """Instruction of using exchange function.

    :arg message: request from bot.

    """
    bot.send_message(message.chat.id,
                     f'Чтобы воспользоваться обменником отправь сообщение вида: \n\n'
                     f'<Имя валюты, цену которой хочешь узнать> <Имя валюты, в которой надо узнать цену первой '
                     f'валюты> <Сумму для перевода> \n\n')
