# coding:utf-8
import web
import os
import time
from sql import *

class MerrySpwier:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)
        self.sql = thesql
        self.lock = False

    def GET(self):
        data = web.input()
        return self.render.merryspwier() 


    def POST(self):
        data = web.input()
        print data
        return self._SaveTheMessage(data['message'],data['name'])
        return self.render.merryspwier()
    
    def _SaveTheMessage(self,message,name):
        if not self.lock:
            if message == "" or name == "":
                return '''<html>
                        <META HTTP-EQUIV="Refresh" CONTENT="1";charset=utf-8" url=//>
                        <meta name="description" content="" />
                        <meta name="keywords" content="" />
                        <!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
                        <script src="/static/js/jquery.min.js"></script>
                        <script src="/static/js/jquery.scrolly.min.js"></script>
                        <script src="/static/js/jquery.poptrox.min.js"></script>
                        <script src="/static/js/skel.min.js"></script>
                        <script src="/static/js/init.js"></script>
                        <div><h1>Please Write down your name and blessing</h1></div></html>'''
            self.lock = True
            self.sql.addzf(name.encode('utf8'),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),message.encode('utf8'))
            self.lock = False
            return '''<html>
                    <META HTTP-EQUIV="Refresh" CONTENT="1";charset=utf-8" url=//>
                    <meta name="description" content="" />
                    <meta name="keywords" content="" />
                    <!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
                    <script src="/static/js/jquery.min.js"></script>
                    <script src="/static/js/jquery.scrolly.min.js"></script>
                    <script src="/static/js/jquery.poptrox.min.js"></script>
                    <script src="/static/js/skel.min.js"></script>
                    <script src="/static/js/init.js"></script>
                    <h1>Save Success !</h1></body></html>'''
        else:
            return '''<html>
                    <META HTTP-EQUIV="Refresh" CONTENT="1";charset=utf-8" url=//>
                    <meta name="description" content="" />
                    <meta name="keywords" content="" />
                    <!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
                    <script src="/static/js/jquery.min.js"></script>
                    <script src="/static/js/jquery.scrolly.min.js"></script>
                    <script src="/static/js/jquery.poptrox.min.js"></script>
                    <script src="/static/js/skel.min.js"></script>
                    <script src="/static/js/init.js"></script>
                    <div><h1>Please Wait....</h1></div></body></html>'''
