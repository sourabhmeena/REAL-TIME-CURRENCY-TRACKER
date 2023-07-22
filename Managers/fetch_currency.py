import os
import time

import aiohttp
from sanic import Sanic, json, text, redirect
from dotenv import load_dotenv
import requests
import csv
from utils import display_currency_handler

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}

currencies = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD',
              'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF',
              'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
              'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL',
              'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES',
              'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL',
              'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN',
              'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR',
              'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD',
              'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX',
              'USD', 'UYU', 'UZS', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF',
              'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL']


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
    try:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=payload, ssl=False) as response:
                result = await response.json()
                rates = result['rates']
                data = []
                for currency, values in rates.items():
                    print(currency, ":", values)
                    data.append({"currency": currency, "value": values, "base": base})

                print(data)

                await store_dict_list_to_csv('data.csv', data)

                time.sleep(interval)

                return await display_currency_handler(not_found_symbol)
    except Exception as e:
        return e


async def fetch_currency_handler(request):
    try:
        print(request)
        # return text("dvd")
        query_params = request.args
        print(query_params)
        # return text("scdc")

        symbols = query_params.get(['symbols'][0], 'USD')
        print(symbols)

        symbols_list = symbols.split(',')

        not_found_symbol =[]
        for val in symbols_list:
            if val not in currencies:
                not_found_symbol.append(val)
        print(not_found_symbol)
        base = query_params.get(['base'][0], 'INR')

        if base not in currencies:
            raise DataNotFoundError('api does not support the base currency you want to send')

        interval = int(query_params.get('interval', 10))

        print(interval)
        data = await asyncio_fetch_currency(symbols, base, interval, not_found_symbol)
        return data

        # TODO: to add infinite call route

        # response = requests.request("GET", url, headers=headers, data=payload)

        # status_code = response.status_code
        # result = response.json()
        # rates = result['rates']
        #
        # data = []
        # for currency, values in rates.items():
        #     print(currency, ":", values)
        #     data.append({"currency": currency, "value": values, "base": base})
        #
        # print(data)
        #
        # await store_dict_list_to_csv('data.csv', data)
        #
        # time.sleep(interval)
        #
        # return json({"status-code": status_code, "result": result})
    except ValueError:
        # If 'amount' is not an integer or not provided, handle the error
        return json({'error': 'Interval must be a integer'}, status=400)
    except DataNotFoundError as e:
        return json({'error': str(e)}, status=404)
    except Exception as e:
        return text(f"Error: {str(e)}")
