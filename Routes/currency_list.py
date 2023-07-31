from sanic import Blueprint,json,text
from requests import Request
from sanic.exceptions import SanicException
from managers.available_currency import avalilable
from managers.remove_currency import remove_from_csv
from managers.exchange_rates import exchange_rates
from managers.convert_currency import convert_currency_handler
from utils.display_currency import *
from models.request import *
currency_list = Blueprint("currency-list", version=1)
# currency = Blueprint('currency',version=2)

@currency_list.get("/convert-currency")
async def convert_currency(request : Request):
    '''
    take input={from,to,amount}
    '''
    try:   #  validator_if_everything_which_is_mandatory_exists
        Convert_Currency_Model(**request.args)
        response = await convert_currency_handler(request)
        return response
    except ValueError as e:
            raise SanicException(f"{str(e)}",status_code=400)



@currency_list.get("/exchange-rates")
async def exchange(request : Request):
    '''
        take input {symbol= country_list , Base= Base_currency and intervel }
    ''' 
    try:   #  validator_if_everything_which_is_mandatory_exists
        Exchange_Rates_Model(**request.args)
        obj=exchange_rates()
        response = await obj.exchange_rates_handler(request)
        return response
    except ValueError as e:
        raise SanicException(f"{str(e)}",status_code=400)


@currency_list.get("/available-currency")
async def available_currency(request):
    response = await avalilable.available_currency_handler(request)
    return response


@currency_list.delete("/remove-currency")
async def remove_currency(request):
    try:  
        Remove_Currency_Model(**request.args)
        response = await remove_from_csv.remove_currency_handler(request)
        return response
    except Exception as e:
        raise SanicException(" Please provide the correct information,  for more info pls go to help page 😇",status_code=400) 

@currency_list.get("/display-currency")
async def display_currency(request):
    response = await Csv_handler.display_currency_handler()
    return response
