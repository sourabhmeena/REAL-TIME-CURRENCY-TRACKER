import asyncio, csv
from sanic import json, text, Request, Sanic
from utils.display_currency import CsvHandler
from crontab import CronTab
from models.valid_currency import ValidCurrency
from .api import Api
from models.response import ExchangeRateResponse
from sanic.exceptions import SanicException
from exceptions.custom_exceptions import *

payload = {}


class ExchangeRate:
    # def __init__(self,base_url) -> None:
    #     self.base_url=base_url

    @classmethod
    async def cronjob_handler(cls, intervel, url):

        cron = CronTab(user='sourabh.meena')
        cron.remove_all()
        job = cron.new(command=f"{url}")
        job.minute.every(intervel)
        cron.write()


    @classmethod
    async def url_for_cron(cls, host, path, valid_symbols, base):
        currency_for_url = valid_symbols[0]
        for val in valid_symbols[1:]:
            currency_for_url = currency_for_url + '%2C' + val
        return f"curl --location 'http:/{host}{path}?symbols={currency_for_url}&base={base}'"


    @classmethod
    async def exchange(cls, symbols, base, invalid_symbols):
        print("async fetch gonna start")
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
            obj = Api(url)
            result = await asyncio.wait_for(obj.api_call(payload), timeout=20)

            rates = result['rates']
            data = []
            for currency, values in rates.items():
                data.append({"currency": currency, "value": values, "base": base})

            await CsvHandler().add_in_csv(data)
            ExchangeRateResponse(**result)
            result["invalid_currencies"] = list(invalid_symbols)
            return json({'status': 200, 'data': result})
        except asyncio.TimeoutError:
            return Exception("Response not received within the timeout period (20 seconds)")
        except Exception as e:
            return SanicException(f'error: {e}', status_code=400)


    @classmethod
    async def exchange_rates_handler(cls, request: Request):
        app = Sanic.get_app()
        try:
            query_params = request.args

            symbols = query_params.get(['symbols'][0], 'USD').upper()
            valid_invalid_symbols = await ValidCurrency(symbols).currency_list_handler()  # dic= {valid_symbols=[],invalid_symbols=[]}

            base = query_params.get(['base'][0], 'INR').upper()
            valid_invalid_base = await ValidCurrency(base).currency_list_handler()

            interval = int(query_params.get(['interval'][0], 1))

            if len(valid_invalid_symbols['valid']) == 0:
                raise DataNotFoundError('Please provide the correct symbols of the Currencies😇', status_code=400)

            if len(valid_invalid_base['valid']) == 0:
                raise DataNotFoundError(message=f'api does not support the base  currency ({base}) you want to fatch',
                                        status_code=400)

            url_for_scheduling = await cls.url_for_cron(request.host, request.path, valid_invalid_symbols['valid'],
                                                        base)
            await cls.cronjob_handler(interval, url_for_scheduling)

            data = app.add_task(cls.exchange(symbols, base, valid_invalid_symbols['invalid']))
            return await data

        except Exception as e:
            return SanicException(f'error: {str(e)}', status_code=400)
