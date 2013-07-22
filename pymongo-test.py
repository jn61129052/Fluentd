#!/usr/bin/env python2.7
import pymongo
from bson.objectid import ObjectId
import datetime
import json


#obj = {u'domain': u'192.168.60.77', u'code': u'404', u'url': u'GET /favicon.ico HTTP/1.1', u'ip': u'192.168.30.24', u'bcode': u'404', u'bsize': u'570', u'nginxtime': u'0.000', u'time': datetime.datetime(2013, 7, 18, 4, 16, 34), u'restime': u'0.000', u'_id': ObjectId('51e76c221d41c81867000020'), u'backend': u'192.168.60.77'}
class MongoConnection():
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def conn(self,db_name,table_name):
        try:
            conn = pymongo.Connection(self.host,self.port)
            if conn:
                db = conn[db_name]
                cursor = db[table_name]
                excute = ""

                for obj in cursor.find():
                    print obj['url']
        except Exception,e:
            print e
        finally:
            conn.close()
             
Conn = MongoConnection('192.168.60.77',27017)
Conn.conn('nginx','access.nginx')
