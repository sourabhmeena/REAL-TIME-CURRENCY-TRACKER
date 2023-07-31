from sanic import Sanic, text,response
import requests_cache
from routes import root_group
from sanic.exceptions import SanicException
# from dotenv import load_dotenv


app = Sanic("currency-tracker")
app.blueprint(root_group)

@app.route("/<path:path>")
async def catch_all(request, path):
    return text(f"Oops! The route '{path}' does not exist.", status=404)

@app.exception(SanicException)
async def handle_sanic_exception(request, exception):
    return response.json({"error": str(exception)}, status=exception.status_code)

if __name__ == '__main__':
    app.run()
