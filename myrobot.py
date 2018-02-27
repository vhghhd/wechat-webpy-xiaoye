#coding=utf-8
import urllib2
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Robot():
    def __init__(self,userid):
        self.url = "http://www.tuling123.com/openapi/api"
        self.apikey = "c7c3ead7262ffd5331f703fae9166563"
        self.userid = userid
        self.codefun = {100000:self._TextClass,
                        200000:self._LinkClass,
                        302000:self._NewsClass,
                        308000:self._BookClass,
                        313000:self._ChildSongClass,
                        314000:self._PoetryClass,
                        40001:self._KeyError,
                        40002:self._InfoEmptyError,
                        40004:self._RequestFull,
                        40007:self._FormatError}
    def SetUserId(self,userid):
        self.userid = userid
    def TalkToMe(self,word):
        #data = self._EncodeRequest(word.encode('utf-8'))
        data = self._EncodeRequest(word)
        ret = self._DecodeData(self._SendToWebRobotPost(data))
        return ret 
    def _EncodeRequest(self,data):
        reqdata = {'key':self.apikey,'info':data,'userid':self.userid}
        return json.dumps(reqdata)
    def _SendToWebRobot(self,data):
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req)
        return response.read()
    def _SendToWebRobotPost(self,data):
        req = urllib2.Request(self.url,data,{'Content-Type':'application/json'})
        response = urllib2.urlopen(req)
        ret = response.read()
        return ret
    def _DecodeData(self,jsdata):
        data = json.loads(jsdata)
        ret = self.codefun[data['code']](data)
        return ret
    def _TextClass(self,data):
        return ('text',data['text'])
    def _LinkClass(self,data):
        return ('link',data['text'],data['url'])
    def _NewsClass(self,data):
        pictures = []
        urls = []
        titles = []
        desps = []
        for li in data['list']:
            urls.append(li['detailurl'])
            pictures.append(li['icon'])
            titles.append(li['article'])
            desps.append(li['article'])
        return ('news',data['text'],urls,titles,pictures,desps)
    def _BookClass(self,data):
        pictures = []
        urls = []
        titles = []
        desps = []
        for li in data['list']:
            urls.append(li['detailurl'])
            pictures.append(li['icon'])
            titles.append(li['name'])
            desps.append(li['info'])
        return ('book',data['text'],urls,titles,pictures,desps)
    def _ChildSongClass(self,data):
        pictures = []
        urls = []
        titles = []
        desps = []
        for li in data['function']:
            urls.append('www.zy.com')
            pictures.append(li['singer'])
            titles.append(li['song'])
            desps.append(li['singer'])
        return ('chsong',data['text'],urls,titles,pictures,desps)
    def _PoetryClass(self,data):
        pictures = []
        urls = []
        titles = []
        desps = []
        for li in data['function']:
            urls.append('www.zy.com')
            pictures.append(li['name'])
            titles.append(li['name'])
            desps.append(li['author'])
        return ('poetry',data['text'],urls,titles,pictures,desps)
    def _KeyError(self,data):
        return ('keyerr',data['text'])
    def _InfoEmptyError(self,data):
        return ('infoerr',data['text'])
    def _RequestFull(self,data):
        return ('reqerr',data['text'])
    def _FormatError(self,data):
        return ('formerr',data['text'])
