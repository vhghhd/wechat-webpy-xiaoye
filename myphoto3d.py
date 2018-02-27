import web
import os

class MyPhoto3D():
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        return self.render.photo3d()

    def POST(self):
        data = web.input()
        return self.render.photo3d()
