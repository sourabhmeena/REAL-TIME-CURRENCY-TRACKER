
from sanic import Blueprint
from Managers.home_page import *
home_route__ = Blueprint("home_route__", version=1)


@home_route__.get('/')
def home_page(request):
    response = home_page_handler(request)
    return response

