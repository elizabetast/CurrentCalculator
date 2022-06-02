"""File of creating tg bot"""
import telebot


TOKEN = "5158217850:AAF6FhYM9bD24LIR67QDI6MDsAMYOyaG9hc"
APPID = "b11fa561d89aaf7aa0e9736f863ffd23"
keys = {
    'USD': 'USD',
    'EUR': 'EUR',
    'RUB': 'RUB',
}
bot = telebot.TeleBot(TOKEN)
