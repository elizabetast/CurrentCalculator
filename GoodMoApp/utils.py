import requests
from config import bot


def get_exchange_rate(src: str):
    """Getting an API of exchange rate
    :arg src: the currency from which to convert.
    :arg dest: the currency to convert to.
    :return: json file with data.
    """
    r = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js').json()
    src.lower()
    if src == 'usd':
        return r['Valute']['USD']['Value']
    elif src == 'eur':
        return r['Valute']['EUR']['Value']

    #return requests.get(f'https://free.currconv.com/api/v7/convert?apiKey=d84cf1bb0ece1d1a78a5&q={src}_{dest}&compact=ultra').json()


def get_wind_direction(deg) -> object:
    """Wind direction data function.
    :arg deg: degree.
    :return: wind direction.
    """
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
    return res
