from sanic import Blueprint

from Managers.available_currency import available_currency_handler
from Managers.remove_currency import remove_currency_handler
from Managers.fetch_currency import fetch_currency_handler
from utils import *

currency_list = Blueprint("currency-list", version=1)


@currency_list.get("/fetch-currency")
async def fetch_currency(request):
    response = await fetch_currency_handler(request)
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
