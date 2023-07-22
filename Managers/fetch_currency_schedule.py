from sanic import Sanic, json, text
import time
import asyncio
import aioschedule as schedule
import aiohttp
import requests
import csv

payload = {}
headers = {
    "apikey": "JknwHsaYjSezamjnreLseIThzME9wwJI"
}


async def store_dict_list_to_csv(file_path, dict_list):
    # Extract the keys from the first dictionary in the list
    fieldnames = dict_list[0].keys()

    # Open the CSV file for writing
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data row by row
        for row in dict_list:
            writer.writerow(row)


async def get_currency(symbols, base):
    print(symbols, base)
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
    async with aiohttp.ClientSession() as session:
        print(url)
        async with session.get(url) as response:
            # return await response.json()
            print(response)

            status_code = response.status_code
            result = response.json()
            rates = result['rates']

            data = []
            for currency, values in rates.items():
                print(currency, ":", values)
                data.append({"currency": currency, "values": values, "base": base})

            print(data)

            await store_dict_list_to_csv('data.csv', data)

            return json({"status-code": status_code, "result": result})


async def send_api_request(symbols, base):
    print("dsvfawd")
    try:
        data = await get_currency(symbols, base)
        print(f"Received data: {data}")
    except aiohttp.ClientError as e:
        print(f"Error during API request: {e}")


async def schedule_task(interval,symbols, base):
    # Schedule the API request to run every interval seconds
    schedule.every(interval).seconds.do(await send_api_request(symbols,base))
    while True:
        try:
            await schedule.run_pending()
        except Exception as e:
            print(f"Error in scheduled task: {e}")
        await asyncio.sleep(1)


async def fetch_currency_handler(request):
    print(request)
    # return text("dvd")
    query_params = request.args
    print(query_params)
    # return text("scdc")

    symbols = query_params['symbols'][0]
    print(symbols)
    base = query_params['base'][0]

    interval = int(query_params.get('interval', 10))

    asyncio.ensure_future(schedule_task(interval,symbols, base))
    return text("Success")
    # asyncio.ensure_future(background_task(symbols, base, interval))
    # url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"
    # return text(url)
    # print(url)
    # return text("dfbntr")
    # num_api_calls= 5
    # for calls in range(num_api_calls-1):
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #
    #     status_code = response.status_code
    #     result = response.json()
    #     rates = result['rates']
    #
    #     data = []
    #     for currency, values in rates.items():
    #         print(currency, ":", values)
    #         data.append({"currency": currency, "values": values})
    #
    #     print(data)
    #
    #     store_dict_list_to_csv('data.csv', data)
    #     time.sleep(interval)

    # response = requests.request("GET", url, headers=headers, data=payload)
    #
    # status_code = response.status_code
    # result = response.json()
    # rates = result['rates']
    #
    # data = []
    # for currency, values in rates.items():
    #     print(currency, ":", values)
    #     data.append({"currency": currency, "values": values, "base": base})
    #
    # print(data)
    #
    # store_dict_list_to_csv('data.csv', data)
    # time.sleep(interval)

    # return json({"status-code": status_code, "result": result})
    # return json(result)
