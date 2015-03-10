# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const
 

class sqlop:
    def __init__(self):
        self.db = web.database(dbn='mysql',host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB)

    def addzf(self,username, fktime, data):
        return self.db.insert('ZhuFu', user=username, time=fktime, data=data)
  
    def get_zfcontent(self,):
        return self.db.select('ZhuFu')

thesql = sqlop()
