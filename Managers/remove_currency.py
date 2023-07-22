import os

from sanic import text, json
import csv
from dotenv import load_dotenv
from utils import display_currency_handler

load_dotenv()

payload = {}
headers = {
    "apikey": os.getenv('API_KEY')
}


class DataNotFoundInCSVError(Exception):
    pass


async def delete_csv_row(file_path, key_column, key_value, not_found_symbol):
    # Read the CSV file and load its contents into memory
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if len(data) == 0:
        raise DataNotFoundInCSVError('The currency you want to remove is not present in the table')

    # Identify the row(s) that need to be deleted
    rows_to_delete = [row for row in data if row[key_column] == key_value]
    print(type(rows_to_delete))

    if len(rows_to_delete) == 0:
        return text('You have entered the currency that is not present in the list, kindly try again')
        # Remove the identified row(s) from the data
    for row in rows_to_delete:
        data.remove(row)

        # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return await display_currency_handler(not_found_symbol)


async def remove_currency_handler(request):
    try:
        print(request)
        # return text("dvd")
        query_params = request.args
        print(query_params)
        not_found_symbol = []
        currency = query_params['currency'][0]
        return await delete_csv_row('data.csv', 'currency', currency, not_found_symbol)
    except DataNotFoundInCSVError as e:
        return json({'error': str(e)}, status=404)
