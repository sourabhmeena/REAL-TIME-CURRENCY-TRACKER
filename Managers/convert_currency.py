import asyncio
from sanic import json,Sanic
from models.valid_currency import Valid_Currency
from .uri_handler import Uri
from models.response import Convert_Currency_Model
from sanic.exceptions import SanicException

class DataNotFoundError(Exception):
    pass


async def asyncio_convert_currency(convert_to, convert_from, amount):
    print("async convert just started")
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
        obj = Uri(url)
        result = await obj.apilayer()
        Convert_Currency_Model(**result)
        return json({"status-code": 200, "result": result})
    
    except Exception as e:
        return SanicException(f'error: {e}',status_code=500)


async def convert_currency_handler(request):
    app=Sanic.get_app()
    try:
        query_params = request.args
        to_=Valid_Currency(query_params['to'][0].upper())     
        from_=Valid_Currency(query_params['from'][0].upper())

        convert_to= await to_.currency_list_handler()   # a valid and invalid list of symbols
        convert_from= await from_.currency_list_handler()

        if len(convert_to['valid']) ==0:
            raise DataNotFoundError(f'We do not support the currency {convert_to["invalid"]} you want to fetch')
        
        if len(convert_from['valid']) ==0:
            raise DataNotFoundError(f'We do not support the currency {convert_from["invalid"]} you want to fetch')
        
        amount = float(query_params.get(['amount'][0],1))
        if amount<=0 :
            raise ValueError("Amount Must be Positive😣")
        return await app.add_task(asyncio_convert_currency(convert_to['valid'][0], convert_from['valid'][0], amount))
    
    except TimeoutError:
        raise Exception("Response not received within the timeout period (20 seconds)")
    except ValueError as e:
        # return json(str(e),status=400)
        return json({'error': 'Only Positive integer and float Values are allowed '}, status=400)
    except Exception as e:
        return json({'error': str(e)}, status=404) 