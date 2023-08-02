from sanic import Sanic, text,response
from routes import root_group
from sanic.exceptions import SanicException
from listeners import Listener

# from dotenv import load_dotenv


app = Sanic("currency-tracker")
app.blueprint(root_group)


# @app.listener("before_server_start")
# async def listener_(app):
#     obj = Listener(app)
#     await obj.check_api()
#     await obj.clear_crontab()


@app.route("/<path:path>")
async def catch_all(request, path):
    return text(f"Oops! The route '{path}' does not exist.", status=404)


@app.exception(SanicException)
async def handle_sanic_exception(request, exception):
    print(exception.status_code)
    print(type(exception))
    print(exception)
    return response.json({"error": str(exception)}, status=exception.status_code)

if __name__ == '__main__':
    app.run()
