import requests


def get_exchange_rate(src: str):
    """Getting an API of exchange rate.

        :arg src: the currency from which to convert.
        :return: json file with data.

        """
    return requests.get(f'https://currate.ru/api/?get=rates&pairs={src}&key=1cbcda852e24af9ee4622153500119ef').json()


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
