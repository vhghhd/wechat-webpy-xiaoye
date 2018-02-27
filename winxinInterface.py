# coding:utf-8
import pylibmc
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import random
from sae import channel
import myrobot
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class WinxinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'template')
        self.render = web.template.render(self.templates_root)
        self.typefunc = {'event':self._event,
                         'text':self._text,
                         'image':self._image,
                         'voice':self._voice,
                         'video':self._video,
                         'location':self._location,
                         'link':self._link,
                         }
        self.datafunc = {'subscribe':self._subscribe,
                         'unsubscribe':self._unsubscribe,
                         'help':self._help,
                         'mus':self._music,
                         'send':self._checkdanmoo,
                         'bye':self._bye,
                         'happy':self._happy,
                         'marry':self._marry,
                         '_rose':self._rose,
						 'game':self._game,
						 'danmoo':self._danmoo,
                         'myson':self._robot,
                         'lovephoto':self._photo3d,
                         'mywedding':self._wedding,
                         }
    def GET(self):
        data = web.input()
        return self._checkuser(data)


    def POST(self):
        str_xml = web.data()
        self.mc = pylibmc.Client()
        return self._checkdata(str_xml)

    def _checkuser(self,data):
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        token = 'zhangyeweixin'

        hashcode = self._hashsha1([token,timestamp,nonce])
        if hashcode == signature:
            return echostr
        else:
            return ""

    def _checkdata(self,data):
        xml = etree.fromstring(data)
        msgType = xml.find('MsgType').text
        try:
            return self.typefunc[msgType](xml)
        except KeyError,e:
            content = e
            fromUser = xml.find('FromUserName').text
            toUser = xml.find('ToUserName').text
            return self.render.reply_text(fromUser,toUser,int(time.time()),content)

    def _event(self,xml):
        mscontent = xml.find("Event").text
        return self.datafunc[mscontent](xml)

    def _subscribe(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'''（输入send进入弹幕模式）\n米娜桑好呀，我是张小烨，这里是我的py微信，哟好好好，输入help查看操作指令''')

    def _unsubscribe(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来')

    def _text(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        try:
            return self.datafunc[mscontent](xml)
        except KeyError,e:
            mcdanmoo = self.mc.get(fromUser+'_danmoo')
            mcrobot = self.mc.get(fromUser+'_robot')
            if mcdanmoo == 'danmoo':
                return self._danmoosend(xml)
            elif mcrobot  == 'robot':
                return self._talktorobot(xml)
            else:
                return self._youdao(xml)

    def _image(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        pass
    def _voice(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        pass
    def _video(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        pass
    def _location(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        pass
    def _link(self,xml):
        mscontent = xml.find("Content").text
        fromUser = xml.find('FromUserName').text
        pass
    def _help(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'''1.输入send进入弹幕模式\n3.输入中文或者英文返回对应的英中翻译''')

    def _hashsha1(self,mlist):
        mlist.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,mlist)
        return sha1.hexdigest()

    def _youdao(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        word = xml.find('Content').text
        if type(word).__name__=='unicode':
            word = word.encode('utf-8')
        qword = urllib2.quote(word)
        baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=vhghhd&key=817509553&type=data&doctype=json&version=1.1&q='
        url = baseurl+qword
        resp = urllib2.urlopen(url)
        fanyi = json.loads(resp.read())
        ##根据json是否返回一个叫“basic”的key来判断是否翻译成功
        if fanyi['errorCode'] == 0:
            if 'basic' in fanyi.keys():
                trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),'\n'.join(fanyi['web'][0]['value']))
            else:
                trans = u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))
            return self.render.reply_text(fromUser,toUser,int(time.time()),trans)
        elif fanyi['errorCode'] == 20:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'对不起，要翻译的文本过长')
        elif fanyi['errorCode'] == 30:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'对不起，无法进行有效的翻译')
        elif fanyi['errorCode'] == 40:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'对不起，不支持的语言类型')
        else:
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'对不起，您输入的单词%s无法翻译,请检查拼写'% word)

    def _music(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text

        musicList = [[r'http://y.qq.com/#type=song&mid=002qU5aY3Qu24y',u'青花瓷',u'Jay Chou'],
                     [r'http://y.qq.com/#type=song&mid=001hH4BK0DjYX5',u'再见',u'Zhenyue Zhang'],
                     [r'http://y.qq.com/#type=song&mid=001WHWFV0K4jVW',u'I Love You',u'Ruolin Wang']]

        music = random.choice(musicList)
        musicTitle = music[1]
        musicDes = music[2]
        musicUrl = music[0]
        return self.render.reply_music(fromUser,toUser,int(time.time()),musicTitle,musicDes,musicUrl)

    def _checkdanmoo(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        mcdanmoo = self.mc.get(fromUser+'_danmoo')
        if mcdanmoo != 'danmoo':
            content = xml.find('Content').text
            self.mc.set(fromUser+'_danmoo','danmoo')
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'进入弹幕模式成功')
        else:
            raise KeyError

    def _bye(self,xml):
        content = xml.find('Content').text
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        mcdanmoo = self.mc.get(fromUser+'_danmoo')
        mcrobot = self.mc.get(fromUser+'_robot')
        if mcdanmoo == 'danmoo':
            self.mc.delete(fromUser+'_danmoo')
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经跳出了弹幕模式，输入help来显示操作指令')
        elif mcrobot == 'robot':
            self.mc.delete(fromUser+'_robot')
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经跳出了小小烨模式，输入help来显示操作指令')
        else:
        	return self._youdao(xml)

    def _danmoosend(self,xml):
        #ask = ask.encode('UTF-8')
        #enask = urllib2.quote(ask)
        #baseurl = r'http://www.simsimi.com/func/req?msg='
        #url = baseurl+enask+'&lc=ch&ft=0.0'
        #resp = urllib2.urlopen(url)
        #reson = json.loads(resp.read())
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        word = xml.find('Content').text
        channel.send_message('danmu',word,True)
        return self.render.reply_text(fromUser,toUser,int(time.time()),u'发射成功！')

    def _happy(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['http://pic20.nipic.com/20120423/5916570_210445658000_2.jpg']
        urls = ['http://1.zhangyewinxin.sinaapp.com/happybirthday']
        titles = [u'张小烨的礼物']
        desp = [u'张小烨的礼物']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)

    def _marry(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['http://1.zhangyewinxin.sinaapp.com/static/images/ten_1.jpg']
        urls = ['http://1.zhangyewinxin.sinaapp.com/']
        titles = [u'大纬 雪卉的结婚请柬']
        desp = [u'大纬 雪卉的结婚请柬']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
    def _rose(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['http://1.zhangyewinxin.sinaapp.com/static/images/rose.jpg']
        urls = ['http://1.zhangyewinxin.sinaapp.com/rose']
        titles = [u'']
        desp = [u'']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
    def _game(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['']
        urls = ['http://1.zhangyewinxin.sinaapp.com/firstgame']
        titles = [u'My Game']
        desp = [u'My Game']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
    def _danmoo(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['']
        urls = ['http://1.zhangyewinxin.sinaapp.com/danmoo']
        titles = [u'My Game']
        desp = [u'My Game']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
    def _robot(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        mcrobot = self.mc.get(fromUser+'_robot')
        if mcrobot  != 'robot':
            content = xml.find('Content').text
            self.mc.set(fromUser+'_robot','robot')
            return self.render.reply_text(fromUser,toUser,int(time.time()),u'进入小小烨模式成功')
        else:
            raise KeyError
    def _robotreturnmany(self,xml,words):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        code = None
        text = None
        pictures = []
        urls = []
        titles = []
        desps = []
        print len(words)
        (code,text,urls,titles,pictures,desps) = words
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desps,pictures,urls)
    def _talktorobot(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        word = xml.find('Content').text
        robot = myrobot.Robot(fromUser)
        #print "zhangye",self.robots[fromUser],fromUser,"zhangye"
        words = robot.TalkToMe(word)
        length = len(words)
        if length == 2:
        	return self.render.reply_text(fromUser,toUser,int(time.time()),words[1])
        elif length == 3:
            return self.render.reply_text(fromUser,toUser,int(time.time()),words[1]+'\n'+words[2])
        else:
            return self._robotreturnmany(xml,words)
    def _photo3d(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['http://1.zhangyewinxin.sinaapp.com/static/images/derryring.jpg']
        urls = ['http://1.zhangyewinxin.sinaapp.com/myphoto3d']
        titles = [u'We Are Family']
        desp = [u'Our Photos']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
    def _wedding(self,xml):
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        picurls = ['http://1.zhangyewinxin.sinaapp.com/static/images/55.jpg']
        urls = ['http://1.zhangyewinxin.sinaapp.com/merryspwier']
        titles = [u'欢迎参加张烨与张莉的婚礼']
        desp = [u'欢迎参加张烨与张莉的婚礼']
        return self.render.reply_news(fromUser,toUser,int(time.time()),1,titles,desp,picurls,urls)
