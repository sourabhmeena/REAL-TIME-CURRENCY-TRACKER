import os
from sanic_ext import render
import aiohttp
import requests
from sanic import json, text
from dotenv import load_dotenv

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


async def asyncio_convert_currency(convert_to, convert_from, amount):
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

        print(request)
        # return text("dvd")
        query_params = request.args
        print(query_params)
        # return text("scdc")

        convert_to = query_params['to'][0]
        if convert_to not in currencies:
            raise DataNotFoundError('api does not support the currency you want to fetch')

        convert_from = query_params['from'][0]
        if convert_from not in currencies:
            raise DataNotFoundError('api does not support the currency you want to fetch')

        # print(symbols)
        amount = int(query_params['amount'][0])

        data = await asyncio_convert_currency(convert_to, convert_from, amount)
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
