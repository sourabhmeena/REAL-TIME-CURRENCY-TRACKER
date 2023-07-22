from sanic_ext import render


async def help_handler(request):
    data = ['there are some commands which even I don\'t know how to run', ' so just copy paste everything']

    return await render("help.html", context={"seq": data}, status=400)
    # return json({"status-code": status_code, "result": result})
    # return json(result)
