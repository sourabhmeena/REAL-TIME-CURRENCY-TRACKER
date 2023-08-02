from sanic_ext import render

# from utils import *


async def home_page_handler(request):
    return await render('home.html')
