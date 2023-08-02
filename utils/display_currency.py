import csv
from sanic import json,text
import asyncio,aiofiles
from sanic.exceptions import BadRequest

class DataNotFoundInCSVError(Exception):
    pass 



class CsvHandler:
    file_path='data.csv'

    @classmethod
    async def add_in_csv(cls, dict_list):
        fieldnames = dict_list[0].keys()
        async with aiofiles.open(cls.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            await writer.writeheader()
            await asyncio.gather(*[writer.writerow(row) for row in dict_list])


    @classmethod
    async def delete_csv_row(cls, key_column, key_value):
        
        with open(cls.file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        if len(data) == 0:
            raise DataNotFoundInCSVError('The list is Empty')

        # Identify the row(s) that need to be deleted
        
        rows_to_save = [row for row in data if row[key_column] != key_value]
        print(rows_to_save)
        # print(rows_to_delete)
        # print(len(rows_to_delete))
        # if len(rows_to_delete) == 0:
        #     raise BadRequest('You have entered the currency that is not present in the list, kindly try again')
        await cls.add_in_csv(rows_to_save)
    
    


    @classmethod
    async def read_data_from_csv(cls,filename):
        
        csv_list = []
        async with aiofiles.open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(await csvfile.readlines())
            csv_list = list(csvreader)
        return csv_list
    


    @classmethod
    async def display_currency_handler(cls):
        
        data = await asyncio.create_task(cls.read_data_from_csv('data.csv'))
        return json(data)
