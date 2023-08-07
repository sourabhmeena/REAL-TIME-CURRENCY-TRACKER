import asyncio
from sanic import json
from .api import Api
from sanic import Sanic
from sanic.exceptions import SanicException
from constants.url import *
payload = {}


class Available:

    @classmethod
    async def fetch_data(cls):
        # url = "https://api.apilayer.com/exchangerates_data/symbols"
        url = Urls.available_currency.value
        obj = Api(url)
        ans = await obj.cached_api_call(payload)
        
        data = ans['symbols']
        currencies = list(data.keys())
        with open('utils/currencies.py', 'w') as f:
            f.write(f"currencies = {currencies}")
        return json(data)
         
    @classmethod
    async def get_data(cls):
        try:
            data = await asyncio.wait_for(cls.fetch_data(), timeout=20)
            return data
        except asyncio.TimeoutError:
            raise Exception("Response not received within the timeout period (20 seconds)")

    @classmethod
    async def available_currency_handler(cls,request):
        app = Sanic.get_app()
        try:
            task = app.add_task(cls.get_data())
            
            data = await task
            return data
        except Exception as e:
            return SanicException(f'error: {e}', status_code=400)
