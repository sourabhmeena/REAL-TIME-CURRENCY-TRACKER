from sanic import Sanic, text, json
import requests_cache
from sanic.exceptions import NotFound
from Routes.root_group import root_group
from dotenv import load_dotenv

load_dotenv()

app = Sanic("currency-tracker")
app.blueprint(root_group)

requests_cache.install_cache('demo_cache', backend="redis", expire_after=86400)


@app.exception(NotFound)
async def not_found(request, exception):
    return text('You entered the wrong URL, kindly check again')


if __name__ == '__main__':
    app.run()
