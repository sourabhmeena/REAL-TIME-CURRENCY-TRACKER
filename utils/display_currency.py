import csv
from sanic_ext import render
from sanic import text


async def read_data_from_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data


async def display_currency_handler(not_found_symbol):
    data = await read_data_from_csv('data.csv')
    print(data)
    # print(len(data))
    # data = [[1,2,3],[4,5,6],[7,8,9]]
    print("verf")
    print(not_found_symbol)
    return await render("display_list.html", context={"seq": data, "not_found_symbol": not_found_symbol, "length": len(not_found_symbol)}, status=200)
