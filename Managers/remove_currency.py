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


class NoQueryParam(Exception):
    pass


async def delete_csv_row(file_path, key_column, key_value):
    # Read the CSV file and load its contents into memory
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if len(data) == 0:
        raise DataNotFoundInCSVError('The list is Empty')

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

    not_found_symbol = []
    return await display_currency_handler(not_found_symbol)


async def remove_currency_handler(request):
    try:
        query_params = request.args

        currency = query_params.get('currency', '-1').upper()
        if currency != '-1':
            return await delete_csv_row('data.csv', 'currency', currency)
        raise NoQueryParam('Kindly enter the currency')
    except NoQueryParam as e:
        return json({'error': str(e)}, status=404)
    except DataNotFoundInCSVError as e:
        return json({'error': str(e)}, status=404)
    except Exception as e:
        return e
