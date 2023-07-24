from sanic import Sanic, text
import requests_cache
from Routes import root_group
# from dotenv import load_dotenv

app = Sanic("currency-tracker")
app.blueprint(root_group)

requests_cache.install_cache('demo_cache', backend="redis", expire_after=86400)


@app.route("/<path:path>")
async def catch_all(request, path):
    return text(f"Oops! The route '{path}' does not exist.", status=404)


if __name__ == '__main__':
    app.run()
