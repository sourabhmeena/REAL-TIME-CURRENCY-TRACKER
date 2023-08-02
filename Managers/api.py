import aiohttp, os
# from sanic import text,json
from dotenv import load_dotenv
from aiohttp_client_cache import CachedSession, SQLiteBackend

load_dotenv()

headers = {
    "apikey": os.getenv('API_KEY')
}


class Api():
    def __init__(self, url) -> None:
        self.url = url

    async def api_call(self, payload={}):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=headers, data=payload, ssl=False) as response:
                    result = await response.json()
                    return result
            except Exception as e:
                return e

    async def cached_api_call(self, payload={}):
        async with CachedSession(cache=SQLiteBackend('demo_cache')) as session:
            try:
                async with session.get(self.url, headers=headers, data=payload, ssl=False) as response:
                    result = await response.json()
                    return result
            except Exception as e:
                return e
