
import telebot

bot = telebot.TeleBot('5158217850:AAF6FhYM9bD24LIR67QDI6MDsAMYOyaG9hc')

USD = 65.38
EUR = 68.94


# /start - выбор валют - вводит сумму в рублях
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
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


bot.polling()

