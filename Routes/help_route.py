from sanic import Blueprint
from sanic import json, text
from Managers.help import help_handler

help_ = Blueprint("help_", version=1)


@help_.get("/help")
async def help__(request):
    response = await help_handler(request)
    return response
