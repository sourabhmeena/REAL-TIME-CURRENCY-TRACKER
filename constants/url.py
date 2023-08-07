from enum import Enum


class Urls(Enum):
    """ url prefixes"""
    available_currency = "https://api.apilayer.com/exchangerates_data/symbols"
    convert_currency = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}"
    exchange_rates = "https://api.apilayer.com/exchangerates_data/latest?symbols={}&base={}"

