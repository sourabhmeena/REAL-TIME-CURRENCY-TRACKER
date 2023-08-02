import asyncio
from sanic import json, Sanic
from models.valid_currency import ValidCurrency
from .api import Api
from models.response import ConvertCurrency
from sanic.exceptions import SanicException


class Convert:
    @classmethod
    async def conversion(cls, convert_to, convert_from, amount):
        print("async convert just started")
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
            obj = Api(url)
            result = await obj.api_call()
            ConvertCurrency(**result)
            return json({"status-code": 200, "result": result})

        except Exception as e:
            return SanicException(f'error: {e}', status_code=400)

    @classmethod
    async def convert_currency_handler(cls, request):
        app = Sanic.get_app()
        try:
            query_params = request.args
            to_ = ValidCurrency(query_params['to'][0].upper())
            from_ = ValidCurrency(query_params['from'][0].upper())

            to_task = to_.currency_list_handler()  # a valid and invalid list of symbols
            from_task = from_.currency_list_handler()
            convert_to, convert_from = await asyncio.gather(*[to_task, from_task], return_exceptions=True)

            if len(convert_to['valid']) == 0:
                raise SanicException(f'We do not support the currency {convert_to["invalid"]} you want to fetch',
                                     status_code=400)

            if len(convert_from['valid']) == 0:
                raise SanicException(f'We do not support the currency {convert_from["invalid"]} you want to fetch',
                                     status_code=400)

            amount = float(query_params.get(['amount'][0], 1))
            if amount <= 0:
                raise ValueError("Amount Must be Positive😣")
            return await app.add_task(cls.conversion(convert_to['valid'][0], convert_from['valid'][0], amount))

        except TimeoutError:
            raise Exception("Response not received within the timeout period (20 seconds)")
        except ValueError as e:
            return json({'error': 'Only Positive integer and float Values are allowed '}, status=400)
        # except Exception as e:
        #     print(e)
        #     return json({'error': str(e)}, status=404)
