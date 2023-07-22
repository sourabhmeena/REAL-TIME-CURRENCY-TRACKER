from sanic import Blueprint
from sanic import json, text
from Managers.convert_currency import convert_currency_handler

convert = Blueprint("convert", version=1)


@convert.get("/convert-currency")
async def convert_currency(request):
    response = await convert_currency_handler(request)
    return response
