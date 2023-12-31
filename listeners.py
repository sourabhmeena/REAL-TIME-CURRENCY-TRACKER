from sanic import json
from managers.api import Api
from crontab import CronTab
from constants.url import *


class Listener:
    def __init__(self, app,loop) -> None:
        self.app = app
        self.loop = loop

    async def check_api(self):
        available_url = Urls.available_currency.value
        obj = Api(available_url)
        res = await obj.api_call()
        if not res.get('success'):
            self.app.stop()
            return json("Api is not working")

    async def clear_crontab(self):
        cron = CronTab(user='sourabh.meena')
        cron.remove_all()
        cron.write()
 