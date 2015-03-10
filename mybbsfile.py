# coding:utf-8
import web
import os
from sql import *

class Bbsfile:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)
        self.sql = thesql

    def GET(self):
        data = web.input()
        data = self.sql.get_zfcontent()
        if data != None:
            return self.render.bbsfile(data)
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
                    <div><h1>暂时还木有祝福哟，抓紧抢楼吧</h1></div></body></html>'''

    def POST(self):
        str_xml = web.data()
        data = self.sql.get_zfcontent()
        if data != None:
            return self.render.bbsfile(data)
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
                    <div><h1>暂时还木有祝福哟，抓紧抢楼吧</h1></div></body></html>'''
