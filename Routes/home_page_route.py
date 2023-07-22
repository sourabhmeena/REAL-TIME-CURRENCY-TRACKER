
from sanic import json, Blueprint

home_route__ = Blueprint("home_route__", version=1)


@home_route__.get('/')
def home_page(request):
    return json({"data": "Welcome to currency tracker, use the /v1/help command to view all the commands"})
