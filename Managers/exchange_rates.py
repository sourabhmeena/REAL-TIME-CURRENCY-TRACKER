import asyncio,csv
from sanic import  json, text, Request,Sanic
from utils.display_currency import Csv_handler
from crontab import CronTab
from models.valid_currency import Valid_Currency
from .uri_handler import Uri
from models.response import Exchange_Rates_Model
from sanic.exceptions import SanicException

payload = {}


class DataNotFoundError(Exception):
    pass

class EmptyList(Exception):
    pass

class exchange_rates():
    # def __init__(self,base_url) -> None:
    #     self.base_url=base_url

    
    async def cronjob_handler(self, intervel,url):
        cron=CronTab(user='soruabh.meena') 
        job=cron.new(command=f'{url}')
        job.minute.every(intervel)
        cron.write()

    async def asyncio_exchange_rates(self,symbols, base, invalid_symbols):
        print("async fetch gonna start")
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

            obj = Uri(url)
            result = await asyncio.wait_for(obj.apilayer(payload),timeout=20)
            rates = result['rates']
            data = []
            for currency, values in rates.items():
                data.append({"currency": currency, "value": values, "base": base})

            await Csv_handler.add_in_csv( data)
            Exchange_Rates_Model(**result)
            result["invalid_currencies"]=list(invalid_symbols)
            return json({'status':200,'data':result})
        except asyncio.TimeoutError:
            return  Exception("Response not received within the timeout period (20 seconds)")
        except Exception as e:
            return SanicException(f'error: {e}',status_code=500)


    
    async def exchange_rates_handler(self,request: Request):
        app=Sanic.get_app()
        try:
            query_params = request.args
            
            symbols = query_params.get(['symbols'][0], 'USD').upper()
            symbols_obj=Valid_Currency(symbols)
            valid_invalid_symbols = await symbols_obj.currency_list_handler()   # dic= {valid_symbols=[],invalid_symbols=[]}
            base = query_params.get(['base'][0], 'INR').upper()
            base_obj=Valid_Currency(base)
            valid_invalid_base = await base_obj.currency_list_handler()

            if len(valid_invalid_symbols['valid']) == 0:
                raise DataNotFoundError('Please provide the correct symbols of the Currencies😇')
            
            if len(valid_invalid_base['valid']) ==0 :
                raise DataNotFoundError(f'api does not support the base  currency ({base}) you want to fatch')

            interval = int(query_params.get('interval', [1])[0])
        
            currency_for_url=valid_invalid_symbols['valid'][0]
            for val in valid_invalid_symbols['valid'][1:]:
                currency_for_url=currency_for_url+'%2C'+val
            
            url_for_scheduling=f"curl --location 'http:/{request.host}{request.path}/?symbols={currency_for_url}&base={base}'"
            
            # print(url_for_scheduling)
            # self.cronjob_handler(interval,url_for_scheduling)

            task1 = app.add_task(self.asyncio_exchange_rates(symbols, base,valid_invalid_symbols['invalid']))
            data = await task1
            return data
        

        except Exception as e:
            return SanicException(f'error: {str(e)}', status_code=404)
   
