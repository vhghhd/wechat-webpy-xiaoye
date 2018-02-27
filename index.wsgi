# coding:utf-8

import os
import sae
import web
from winxinInterface import WinxinInterface
from myindex import Index
from happybday import HappyBirthday
from mysrc import MySrc
from myphoto import Photo
#from mybbsfile import Bbsfile
from myrose import Rose
from chatactoe import TheXOGame
from mydanmoo import Danmoo
from myxml import Xml
from myphoto3d import MyPhoto3D
from mywedding import MerrySpwier

urls = (
			'/','Index',
			'/weixin','WinxinInterface',
			'/happybirthday','HappyBirthday',
			'/photo*', 'Photo',
            '/rose','Rose',
			'/firstgame*','TheXOGame',
			#'/firstgame/opened*','TheXOGame',
			'/firstgame/(.*?)','TheXOGame',
            #'/bbsfile*', 'Bbsfile',
			'/danmoo','Danmoo',
            '/xml','Xml',
            '/myphoto3d','MyPhoto3D',
	    '/merryspwier','MerrySpwier',
)

app_root=os.path.dirname(__file__)
templates_root = os.path.join(app_root,'template')
app = web.application(urls,globals()).wsgifunc()
application = sae.create_wsgi_app(app)
