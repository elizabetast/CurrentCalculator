from config import bot
from texts import KeyboardTexts
from handlers import converter, exchange_currency, request_forecast, request_available_currency, show_cit

"""Starting bot and buttons functions."""

if __name__ == "__main__":
    bot.register_message_handler(request_forecast, regexp=KeyboardTexts.WEATHER)
    bot.register_message_handler(converter, regexp="[A-Z]{3} [A-Z]{3} \d+")
    bot.register_message_handler(request_available_currency, regexp=KeyboardTexts.CURRENCY_RATE)
    bot.register_message_handler(request_available_currency, commands=["values"])
    bot.register_message_handler(exchange_currency, commands=["help"])
    bot.register_message_handler(exchange_currency, regexp=KeyboardTexts.EXCHANGE_CURRENCY)
    bot.register_message_handler(show_cit, regexp=KeyboardTexts.CITS)
    bot.register_message_handler(show_cit, commands=["quote"])
    bot.polling(none_stop=True)
