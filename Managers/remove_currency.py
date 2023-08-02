from sanic import json, text
from utils.display_currency import CsvHandler
from exceptions.custom_exceptions import *


class RemoveFromCsv:

    @classmethod
    async def remove_currency_handler(cls, request):
        try:
            query_params = request.args
            currency = query_params.get(['currency'][0]).upper()
            currency_list = currency.split(',')
            # print(currency_list)
            await CsvHandler.delete_csv_row('currency', currency_list)

            return await CsvHandler.display_currency_handler()

        except NoQueryParam as e:
            return json({'error': str(e)}, status=404)
        except DataNotFoundInCSVError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return json({'error': str(e)}, status=404)
