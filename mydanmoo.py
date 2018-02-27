import web
import os
from sae import channel
import time

class Danmoo():
    url = ''
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)
        self.url = channel.create_channel('danmu',10)

    def GET(self):
        data = web.input()
        return self.render.danmoo(self.url)

    def POST(self):
        data = web.input()
        return self.render.danmoo(self.url)