from sanic_ext import render


async def help_handler(request):
    data = []
    return await render("help.html", context={"seq": data}, status=400)

