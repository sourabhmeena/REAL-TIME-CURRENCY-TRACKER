from sanic import Blueprint, json, text
from requests import Request
from sanic.exceptions import SanicException
from managers.available_currency import Available
from managers.remove_currency import RemoveFromCsv
from managers.exchange_rates import ExchangeRate
from managers.convert_currency import Convert
from utils.display_currency import *
from models.request import *

currency_list = Blueprint("currency-list", version=1)


# currency = Blueprint('currency',version=2)

@currency_list.get("/convert-currency")
async def convert_currency(request: Request):
    '''
    take input={from,to,amount}
    '''
    try:
        ConvertCurrency(**request.args)
        response = await Convert().convert_currency_handler(request)
        return response
    except ValueError as e:
        raise SanicException(f"{str(e)}", status_code=400)


@currency_list.get("/exchange-rates")
async def exchange(request: Request):
    '''
        take input {symbol= country_list , Base= Base_currency , interval }
    '''
    try:
        ExchangeRates(**request.args)
        response = await ExchangeRate().exchange_rates_handler(request)
        return response
    except Exception as e:
        raise SanicException(f"{str(e)}", status_code=400)


@currency_list.get("/available-currency")
async def available_currency(request):
    response = await Available.available_currency_handler(request)
    return response


@currency_list.delete("/remove-currency")
async def remove_currency(request):
    try:
        RemoveCurrencyModel(**request.args)
        response = await RemoveFromCsv.remove_currency_handler(request)
        return response
    except Exception as e:
        raise SanicException(f"{str(e)}", status_code=400)


@currency_list.get("/display-currency")
async def display_currency(request):
    response = await CsvHandler.display_currency_handler()
    return response
