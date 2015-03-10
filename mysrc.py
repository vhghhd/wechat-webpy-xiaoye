import web
import os

class MySrc:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'src')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        return self.render.happy()

    def POST(self):
        data = web.input()
        return self.render.happy()
