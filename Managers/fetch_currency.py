import asyncio
import os
import time
import aiohttp
from sanic import Sanic, json, text, redirect
from dotenv import load_dotenv
import csv
from utils import display_currency_handler, currencies

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class DataNotFoundError(Exception):
    pass


async def store_dict_list_to_csv(file_path, dict_list):
    # Extract the keys from the first dictionary in the list
    fieldnames = dict_list[0].keys()

    # Open the CSV file for writing
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data row by row
        for row in dict_list:
            writer.writerow(row)


async def asyncio_fetch_currency(symbols, base, interval, not_found_symbol):
    print("async fetch gonna start")
    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                result = await response.json()
                rates = result['rates']
                data = []
                for currency, values in rates.items():
                    # print(currency, ":", values)
                    data.append({"currency": currency, "value": values, "base": base})

                # print(data)

                await store_dict_list_to_csv('data.csv', data)

                # time.sleep(1)

                return await display_currency_handler(not_found_symbol)
    except Exception as e:
        return e


# async def trial(symbols, base, interval, not_found_symbol):
#     while True:
#         # Wait for 10 seconds
#         print("Scheduled make_api_call task started")
#         await asyncio_fetch_currency(symbols, base, interval, not_found_symbol)
#         print("Scheduled make_api_call task completed")
#         await asyncio.sleep(interval)
#

async def fetch_currency_handler(request):
    try:
        # print(request)
        # return text("dvd")
        query_params = request.args
        # print(query_params)
        # return text("scdc")

        symbols = query_params.get(['symbols'][0], 'USD')
        # print(symbols)

        symbols_list = symbols.split(',')

        not_found_symbol = []
        for val in symbols_list:
            if val not in currencies:
                not_found_symbol.append(val)
        # print(not_found_symbol)
        base = query_params.get(['base'][0], 'INR')

        if base not in currencies:
            raise DataNotFoundError('api does not support the base currency you want to send')

        interval = int(query_params.get('interval', 60))

        # print(interval)
        print("fetch_task gonna start")
        # data = await asyncio_fetch_currency(symbols, base, interval, not_found_symbol)
        task1 = asyncio.create_task(asyncio_fetch_currency(symbols, base, interval, not_found_symbol))
        # task1 = asyncio.create_task(trial(symbols, base, interval, not_found_symbol))
        # return data
        data = await task1
        print("fetch_task_end")
        return data

    except ValueError:
        # If 'amount' is not an integer or not provided, handle the error
        return json({'error': 'Interval must be a integer'}, status=400)
    except DataNotFoundError as e:
        return json({'error': str(e)}, status=404)
    except Exception as e:
        return text(f"Error: {str(e)}")
