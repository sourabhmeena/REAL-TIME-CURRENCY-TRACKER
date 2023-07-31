
from sanic import Blueprint
from utils.home_page import home_page_handler
from utils.help import help_handler
home_bp = Blueprint("home_route__", version=1)


@home_bp.get("/")
def home_page(request):
    response = home_page_handler(request)
    return response

@home_bp.get("/help")
async def help__(request):
    response = await help_handler(request)
    return response

