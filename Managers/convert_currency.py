import asyncio
import os
from sanic_ext import render
import aiohttp
import requests
from sanic import json, text
from dotenv import load_dotenv
from utils import currencies

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class DataNotFoundError(Exception):
    pass


async def asyncio_convert_currency(convert_to, convert_from, amount):
    print("async convert just started")
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                result = await response.json()
                return json({"status-code": 200, "result": result})
    except Exception as e:
        return e


async def convert_currency_handler(request):
    try:

        # print(request)
        # return text("dvd")
        query_params = request.args
        # print(query_params)
        # return text("scdc")

        convert_to = query_params['to'][0]
        if convert_to not in currencies:
            raise DataNotFoundError('api does not support the currency you want to fetch')

        convert_from = query_params['from'][0]
        if convert_from not in currencies:
            raise DataNotFoundError('api does not support the currency you want to fetch')

        # print(symbols)
        amount = int(query_params['amount'][0])

        print("convert_currency gonna start")
        task2 = asyncio.create_task(asyncio_convert_currency(convert_to, convert_from, amount))

        data = await task2
        print("convert_currency_end")
        return data

        # return text(url)
        # print(url)
        # return text("dfbntr")
        # response = requests.request("GET", url, headers=headers, data=payload)
        #
        # status_code = response.status_code
        # result = response.json()
        # return json({"status-code": status_code, "result": result})
        # return json(result)
    except ValueError:
        # If 'amount' is not an integer or not provided, handle the error
        return json({'error': 'amount must be a integer'}, status=400)
    except DataNotFoundError as e:
        return json({'error': str(e)}, status=404)
    except Exception as e:
        return text(f"Error: {str(e)}")
