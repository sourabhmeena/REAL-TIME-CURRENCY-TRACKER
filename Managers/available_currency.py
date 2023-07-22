import os
import requests
import json
import sanic
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
            print(type(ans))
            print(ans)
            data = ans.get('symbols')
            return await render("available.html", context={"seq": data}, status=200)


async def get_data_with_timeout(request):
    try:
        # Set the timeout to 10 seconds
        data = await asyncio.wait_for(fetch_data(request), timeout=20)
        return data
    except asyncio.TimeoutError:
        raise Exception("Response not received within the timeout period")


async def available_currency_handler(request):
    try:
        data = await get_data_with_timeout(request)
        return data
    except Exception as e:
        return text(f"Error: {str(e)}")
        # url = f"https://api.apilayer.com/exchangerates_data/symbols"
        #
        # response = requests.request("GET", url, headers=headers, data=payload)
        #
        # status_code = response.status_code
        # result = response.json()
        # data = result['symbols']
        #
        # # with open('template.html', 'r') as file:
        # #     html_template = file.read()
        # #
        # # json_data_Html = "<pre>" + json.dumps(data) + "</pre>"
        # # rendered_html = html_template.replace('jsonData', json_data_Html)
        #
        # return await render("available.html", context={"seq": data}, status=400)
