import datetime

import telebot
from pycbrf import ExchangeRates

bot = telebot.TeleBot('5158217850:AAF6FhYM9bD24LIR67QDI6MDsAMYOyaG9hc')

USD = 65.38
'''нужно подключение к реальному курсу'''
EUR = 68.94

@bot.message_handler(commands=['start']) #отслеживание команды старта и вообще команд
def start(message):
    mess = f'Привет, <b><u>{message.from_user.first_name}</u></b>! Чтобы начать работу с ботом, введите /help ' \
           f' и ознакомьтесь с доступными командами.'
    bot.send_message(message.chat.id, mess, parse_mode='html') #функция для привестсвия (???как в хтмл сделать перенос троки???)

@bot.message_handler(commands=['help'])
def help(message):
    mess = f'/transfer - команда перевода валюты'
    bot.send_message(message.chat.id, mess, parse_mode='html')

# выбор валют - вводит сумму в рублях
@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == '/transfer':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('€', '$')
        msg = bot.send_message(message.chat.id, 'Выберите валюту',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, currency)


def currency(message):
    if message.text == '€':
        msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
        bot.register_next_step_handler(msg, eur)
    elif message.text == '$':
        msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
        bot.register_next_step_handler(msg, usd)

    else:
        msg = bot.send_message(message.chat.id, "Введите корректные данные")
        bot.register_next_step_handler(msg, currency)


def eur(message):
    try:
        bot.send_message(message.chat.id, float(message.text) / EUR)
    except ValueError:
        bot.send_message(message.chat.id, "Введите число")


def usd(message):
    try:
        bot.send_message(message.chat.id, float(message.text) / USD)
    except ValueError:
        bot.send_message(message.chat.id, "Введите число")


bot.polling(none_stop=True)

@bot.message_handler(commands=['quit']) #функция выхода из бота в дефолтное состояние или это не функция должна быть
def quit(message):
    mess = f'/transfer - команда перевода валюты'
    bot.send_message(message.chat.id, mess, parse_mode='html')
'''
@bot.message_handler(commands=['start']) #отслеживание команды старта и вообще команд
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    it1 = telebot.types.KeyboardButton('USD')
    it2 = telebot.types.KeyboardButton('EUR')
    markup.add(it1,it2)
    mess = f'Выберите валюту'
    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html') #чтобы бот отправлял сообщение Привет

@bot.message_handler(content_types=['text'])
def message(message):
    mess_norm = message.text.strip().lower()
    if mess_norm in ['usd','eur']:
        rates = ExchangeRates(datetime.now())
        mess = f'Курс такой {float(rates)}'
        bot.send_message(message.chat.id, mess, parse_mode='html')


bot.polling()
'''