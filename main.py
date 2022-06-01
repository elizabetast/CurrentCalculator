import telebot
import requests
import json
from config import keys, TOKEN, APPID
import pb

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               row_width=2)
    itembtn1 = telebot.types.KeyboardButton("Погода")
    itembtn2 = telebot.types.KeyboardButton("Курсы валют")
    itembtn3 = telebot.types.KeyboardButton("Перевод валют")
    markup.add(itembtn1, itembtn2, itembtn3)
    msg = bot.send_message(message.chat.id,
                           f"Привет, {message.chat.username}.\n  Выберите действие.",
                           reply_markup=markup)

    bot.register_next_step_handler(msg, process_switch_step)


def process_switch_step(message):
    if message.text == "Погода":
        request_current_weather(message)
        welcome_message(message)
    elif message.text == "Курсы валют":
        value(message)
        welcome_message(message)
    elif message.text == "Перевод валют":
        values_message(message)


def get_wind_direction(deg) -> object:
    l = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
    for i in range(0, 8):
        step = 45.
        min = i * step - 45 / 2.
        max = i * step + 45 / 2.
        if i == 0 and deg > 360 - 45 / 2.:
            deg = deg - 360
        if min <= deg <= max:
            res = l[i]
            break
    #return res


@bot.message_handler(content_types=['text', ])
# Запрос текущей погоды
def request_current_weather(message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': 519690, 'units': 'metric',
                                   'lang': 'ru', 'APPID': APPID})

        data = res.json()
        texts = {"conditions:": data['weather'][0]['description'],
                 "temp:": data['main']['temp'],
                 "temp_min:": data['main']['temp_min'],
                 "temp_max:": data['main']['temp_max'],
                 }
        result = []
        for i, j in texts.items():
            result.append(str(i) + ' ' + str(j))
        bot.send_message(message.chat.id, '\n'.join(result))
    except Exception as e:
        bot.reply_to(message, f'Погода не найдена.\n{e}')


"""
@bot.message_handler(content_types=['text', ])
# Прогноз
def request_forecast(message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': 519690, 'units': 'metric',
                                   'lang': 'ru', 'APPID': APPID})
        data = res.json()

        for i in data['list']:
            w = (i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']),
            f'{i["wind"]["speed"]:2.0f}' + " м/с",
            get_wind_direction(i['wind']['deg']),
            i['weather'][0]['description']

            bot.send_message(message.chat.id, w)
    except Exception as e:
        bot.reply_to(message, f'Погода не найдена.\n{e}')
"""


def values_message(message):
    bot.send_message(message.chat.id,
                     f'Чтобы воспользоваться ботом отправь сообщение вида: \n\n'
                     f'<Имя валюты, цену которой хочешь узнать> <Имя валюты, в которой надо узнать цену первой валюты> <Сумму для перевода> \n\n')


def value(message):
    """Функция курса"""
    text = f'Доступные валюты: \n' \
           f'USD = {pb.resUSD} \n ' \
           f'EUR = {pb.resEUR}'

    bot.send_message(message.chat.id, text)  # вывод


class ConvertionExeption(Exception):
    pass


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')  # проверка что введено три параметра

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
        total_base = list(total_base.value())
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {quote} = {round(float(*total_base), 3) * amount} {base} '  # вывод подсчётов
        bot.send_message(message.chat.id, text)
    welcome_message(message)


bot.polling(none_stop=True)
