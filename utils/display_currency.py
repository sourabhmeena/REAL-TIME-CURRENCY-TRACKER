import csv
from sanic import json,text
import asyncio,aiofiles

class DataNotFoundInCSVError(Exception):
    pass 

class Csv_handler:
    file_path='data.csv'
    @classmethod
    async def delete_csv_row(cls, key_column, key_value):

        with open(cls.file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        if len(data) == 0:
            raise DataNotFoundInCSVError('The list is Empty')

        # Identify the row(s) that need to be deleted
        rows_to_delete = [row for row in data if row[key_column] == key_value]
        print(type(rows_to_delete))

        if len(rows_to_delete) == 0:
            return text('You have entered the currency that is not present in the list, kindly try again')
        
        for row in rows_to_delete:
            data.remove(row)

        async with aiofiles.open(cls.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(data)

    
    @classmethod
    async def add_in_csv(cls, dict_list):
        fieldnames = dict_list[0].keys()
        async with aiofiles.open(cls.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in dict_list:
                writer.writerow(row)


    @classmethod
    async def read_data_from_csv(cls,filename):
        csv_list = []
        async with aiofiles.open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            csv_list = list(csvreader)
        return csv_list
    


    @classmethod
    async def display_currency_handler(cls):
        data = await asyncio.create_task(cls.read_data_from_csv('data.csv'))
        return json(data)
