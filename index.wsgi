# coding:utf-8

import os
import sae
import web
from winxinInterface import WinxinInterface
from myindex import Index
from happybday import HappyBirthday
from mysrc import MySrc
from myphoto import Photo
from mybbsfile import Bbsfile

urls = (
			'/','Index',
			'/weixin','WinxinInterface',
			'/happybirthday','HappyBirthday',
			'/photo*', 'Photo',
            '/bbsfile*', 'Bbsfile'
)
app_root=os.path.dirname(__file__)
templates_root = os.path.join(app_root,'template')
app = web.application(urls,globals()).wsgifunc()
application = sae.create_wsgi_app(app)
