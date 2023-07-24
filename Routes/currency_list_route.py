from sanic import Blueprint

from Managers.available_currency import available_currency_handler
from Managers.remove_currency import remove_currency_handler
from Managers.exchange_rates import exchange_rates_handler
from utils import *
from sanic.response import text,json
currency_list = Blueprint("currency-list", version=1)


@currency_list.get("/exchange-rates")
async def exchange_rates(request):                       #
    response = await exchange_rates_handler(request)
    return response


@currency_list.get("/available-currency")
async def available_currency(request):
    response = await available_currency_handler(request)
    return response


@currency_list.get("/remove-currency")
async def remove_currency(request):
    response = await remove_currency_handler(request)
    return response


@currency_list.get("/display-currency")
async def display_currency(request):
    response = await display_currency_handler()
    return response
