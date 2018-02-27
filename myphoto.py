# coding:utf-8
import web
import os

class Photo:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        return self.render.photos() 


    def POST(self):
        str_xml = web.data()
        return self.render.photos() 
