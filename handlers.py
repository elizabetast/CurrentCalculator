import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import requests
from datetime import datetime

from config import bot, APPID, keys
from exceptions import ConvertionException
from utils import get_wind_direction, get_exchange_rate
from texts import KeyboardTexts

import openpyxl
import random

import utils


@bot.message_handler(commands=['start'])
def welcome_message(message):
    """Start interface function.

            :arg message: request from bot.
            :return: hello message.

        """
    markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                 row_width=2)
    weather_button = KeyboardButton(KeyboardTexts.WEATHER)
    currency_rate_button = KeyboardButton(KeyboardTexts.CURRENCY_RATE)
    exchange_currency_button = KeyboardButton(KeyboardTexts.EXCHANGE_CURRENCY)
    random_cits_button = KeyboardButton(KeyboardTexts.CITS)
    markup.add(weather_button, currency_rate_button, exchange_currency_button, random_cits_button)
    bot.send_message(message.chat.id,
                     f"Доброе утро, {message.chat.username}!🥐\n\nКоманда Good Mo желает тебе прекрасного дня.\n\n"
                     f"Начни своё утро с просмотра погоды на весь день и ответа на вопрос ?менять или не менять?""\n\n Для начала выбери действие.",
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
        today_forecast = list(filter(
            lambda x: datetime.strptime(x["dt_txt"][:10],
                                        "%Y-%m-%d").day == today,
            data['list']))
        result = ["🌥 Погода на сегодня\n"]
        for i in today_forecast:
            time = datetime.strptime(i["dt_txt"],
                                     "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            result.append(
                f"⏰ {time}:\n🌡 {i['main']['temp']} °C\n💨 {str(i['wind']['speed'])}м/с. {i['weather'][0]['description']} \n Направление: {get_wind_direction(i['wind']['deg'])}\n")

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
            raise ConvertionException('Неправильные параметров.')

        quote, base, amount = values

        if quote not in keys:
            raise ValueError(f'Не удалось обработать валюту {quote}')

        if base not in keys:
            raise ValueError(f'Не удалось обработать валюту {base}')

        if quote == base:
            raise ConvertionException(
                f'Невозможно перевести одинаковые валюты {base}')

        rate = float(
            utils.get_exchange_rate(quote + base)['data'][quote + base])

    except ValueError as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    else:
        text = f'{amount} {quote} = {rate * float(amount)} {base} '  # вывод подсчётов
        bot.send_message(message.chat.id, text)


def request_available_currency(message: telebot.types.Message):
    """Function showing list of available currency.

        :arg message: request from bot.
        :return: message list of currency.

        """
    bot.send_message(message.chat.id, f'Доступные валюты: \n' \
                                      f'🇬🇧 USD = {get_exchange_rate("USDRUB")["data"]["USDRUB"]} RUB \n' \
                                      f'🇪🇺 EUR = {get_exchange_rate("EURRUB")["data"]["EURRUB"]} RUB \n' \
                                      f'🇧🇾 BYN = {get_exchange_rate("BYNRUB")["data"]["BYNRUB"]} RUB ')


def exchange_currency(message: telebot.types.Message):
    """Instruction of using exchange function.

        :arg message: request from bot.
        :return instruction for exchanger.

        """
    bot.send_message(message.chat.id,
                     f'Чтобы воспользоваться обменником отправь сообщение вида: \n\n'
                     f'<Имя валюты, сумму которой хочешь узнать> <Имя валюты, в которой надо узнать сумму первой '
                     f'валюты> <Сумму для перевода> \n\n'
                     f'Например: EUR RUB 100\n\n '
                     )


def show_cit(message: telebot.types.Message):
    """Random quote output function.

            :arg message: request from bot.
            :return random quote.

            """
    now = datetime.now()
    cit_arr = []
    flag = 0
    table = openpyxl.reader.excel.load_workbook(filename="cit.xlsx")
    table.active = 0
    sheet = table.active
    for i in range(1, 52):
        cit = sheet['A' + str(i)].value
        cit_arr.append(cit)
    random_cit = random.choice(cit_arr)
    if flag == 0:
        bot.send_message(message.chat.id, random_cit)
        flag += 1
    elif flag > 0:
        bot.send_message(message.chat.id, "Хватит")
