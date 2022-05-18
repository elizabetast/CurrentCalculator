from _datetime import datetime

import telebot
from pycbrf import ExchangeRates

bot = telebot.TeleBot('5158217850:AAF6FhYM9bD24LIR67QDI6MDsAMYOyaG9hc')



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
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        but1 = telebot.types.KeyboardButton('USD')
        but2 = telebot.types.KeyboardButton('EUR')
        markup.add(but1, but2) #создание кнопок
        msg = bot.send_message(chat_id=message.chat.id, text=f'Выберите валюту', reply_markup=markup, parse_mode='html')#вывод на экран предложения о переводе валюты
        bot.register_next_step_handler(msg, currency) #для того чтобы вызывать другие функции


def currency(message):
    if message.text == 'EUR':
        msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
        bot.register_next_step_handler(msg, course)
    elif message.text == 'USD':
        msg = bot.send_message(message.chat.id, "Введите сумму в рублях")
        bot.register_next_step_handler(msg, course)
    else:
        msg = bot.send_message(message.chat.id, "Введите корректные данные")
        bot.register_next_step_handler(msg, currency)

def course(message): #функция находжения курса
    mess_norm = message.text.strip().lower()
    bot.send_message(chat_id=message.chat.id, mess_norm)

    if mess_norm == 'usd': #если мы выбрали что-то из этого
        rates = ExchangeRates(datetime.now())
        res = float(rates[mess_norm.upper()].rate) #это сам курс доллара
        bot.send_message(message.chat.id, float(message.text))
    elif mess_norm == 'eur':
        rates = ExchangeRates(datetime.now())
        res = float(rates[mess_norm.upper()].rate) #это сам курс евро
        bot.send_message(message.chat.id, float(message.text))
    else:
        bot.send_message(message.chat.id, "Введите число")
'''
def eur(message):
    try:
        bot.send_message(message.chat.id, float(message.text))
    except ValueError:
        bot.send_message(message.chat.id, "Введите число")


def usd(message):
    try:
        bot.send_message(message.chat.id, float(message.text))
    except ValueError:
        bot.send_message(message.chat.id, "Введите число")

'''
bot.polling(none_stop=True)

@bot.message_handler(commands=['quit']) #функция выхода из бота в дефолтное состояние или это не функция должна быть
def quit(message):
    mess = f'/transfer - команда перевода валюты'
    bot.send_message(message.chat.id, mess, parse_mode='html')

#код получения курса в реальном времени и его вывода в боте
'''
@bot.message_handler(commands=['course']) #отслеживание команды старта и вообще команд
def course(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    it1 = telebot.types.KeyboardButton('USD')
    it2 = telebot.types.KeyboardButton('EUR')
    markup.add(it1,it2)
    bot.send_message(chat_id= message.chat.id, text=f'Выберите валюту', reply_markup=markup, parse_mode='html') #чтобы бот отправлял сообщение Привет

@bot.message_handler(content_types=['text'])
def message(message):
    mess_norm = message.text.strip().lower()
    if mess_norm in ['usd','eur']:
        rates = ExchangeRates(datetime.now())
        bot.send_message(chat_id=message.chat.id, text=f'<b>{mess_norm.upper()} rate is {float(rates[mess_norm.upper()].rate)}</b>', parse_mode='html')


bot.polling(none_stop=True)
'''