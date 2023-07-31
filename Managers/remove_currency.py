from sanic import  json,text
from utils.display_currency import Csv_handler


class DataNotFoundInCSVError(Exception):
    pass


class NoQueryParam(Exception):
    pass

class remove_from_csv:

    @classmethod
    async def remove_currency_handler(self,request):
        try:
            query_params = request.args

            currency = query_params.get('currency').upper()
            
            currency_list=currency.split(',')
            print(currency_list) 
            for currency in currency_list:
                 await Csv_handler.delete_csv_row( 'currency', currency)
            
            return  await Csv_handler.display_currency_handler()
            
        except NoQueryParam as e:
            return json({'error': str(e)}, status=404)
        except DataNotFoundInCSVError as e:
            return json({'error': str(e)}, status=404)
        except Exception as e:
            return e
