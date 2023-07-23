import os
import asyncio
import aiohttp
from sanic import text
from dotenv import load_dotenv
from sanic_ext import render

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


async def fetch_data(request):
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=payload,ssl=False) as response:
            ans = await response.json()
            data = ans.get('symbols')
            return await render("available.html", context={"seq": data}, status=200)


async def get_data_with_timeout(request):
    try:
        # Set the timeout to 60 seconds
        data = await asyncio.wait_for(fetch_data(request), timeout=60)
        return data
    except asyncio.TimeoutError:
        raise Exception("Response not received within the timeout period (60 seconds)")


async def available_currency_handler(request):
    try:
        task3 = asyncio.create_task(get_data_with_timeout(request))
        data = await task3
        return data
    except Exception as e:
        return text(f"Error: {str(e)}")

