#-*- coding: gbk -*-
#coding=gbk 
#!/usr/bin/env python2.7
import pymongo
from bson.objectid import ObjectId
import datetime
import re
import sys
import time


#obj = {u'domain': u'192.168.60.77', u'code': u'404', u'url': u'GET /favicon.ico HTTP/1.1', u'ip': u'192.168.30.24', u'bcode': u'404', u'bsize': u'570', u'nginxtime': u'0.000', u'time': datetime.datetime(2013, 7, 18, 4, 16, 34), u'restime': u'0.000', u'_id': ObjectId('51e76c221d41c81867000020'), u'backend': u'192.168.60.77'}
class MongoConnection():
    def __init__(self):
        self.host = "192.168.60.77"
        self.port = 27017
        self.db_name = "nginx"
        self.table_name = "access.nginx"
        self.ng1_count = 0
        self.be1_count = 0
        self.total_count = 0
        self.total_backtime = 0
        self.total_bodysize = 0
        self.total_nginxtime = 0
        self.fxx_count = 0
        self.ng3_count = 0
        self.be3_count = 0
        self.too_count = 0
        self.sxx_count = 0
        
        
    #nginx响应时间超过1秒个数
    def count_ng1(self,obj):
        if obj is not None:
            if float(obj["nginxtime"]) >= 1.0:
                ng1_count += 1
    
    #backend后端响应时间超过1秒个数
    def count_be1(self,obj):
        if obj is not None:
            if float(obj["restime"]) >= 1.0:
                self.be1_count += 1
    
    #过去5分钟该域名的请求总数
    def count_total(self,domain):
        self.total_count = self.cursor.find({"domain":domain}).count()
    
    #backend后端响应时间总和 
    def backtime_total(self,obj):
        if obj is not None:
            self.total_backtime += float(obj["restime"])
    
    #4xx请求个数
    def count_fxx(self,obj):
        regex = re.compile(r'4\d\d')
        if obj is not None:
            if regex.search(obj["code"]):
                self.fxx_count += 1
                
     
    #bodysize总和
    def bodysize_total(self,obj):
        if obj is not None:
            self.total_bodysize += int(obj["bsize"])
            
    #nginx请求总时间大于3秒的请求个数
    def count_ng3(self,obj):
        if obj is not None:
            if float(obj["nginxtime"]) + float(obj["restime"]) >= 3.0:
                self.ng3_count += 1
    
    #200请求个数
    def count_too(self,obj):
        regex = re.compile(r'2\d\d')
        if obj is not None:
            if regex.search(obj["code"]):
                self.too_count += 1
    
    #5xx请求个数
    def count_sxx(self,obj):
        regex = re.compile(r'5\d\d')
        if obj is not None:
            if regex.search(obj["code"]):
                self.sxx_count += 1
    
    #nginx请求总时间
    def nginxtime_total(self,obj):
        if obj is not None:
            self.total_nginxtime += float(obj["nginxtime"])
            
    #backend响应时间超过3秒的个数
    def count_be3(self,obj):
        if obj is not None:
            if float(obj["restime"]) >= 3.0:
                self.be3_count += 1
    #获取5分钟前的时间
    def five_time(self):
        start = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        end = datetime.datetime.utcnow()
        return start,end

    def conn(self):
        try:
            self.conn = pymongo.Connection(self.host,self.port)
            if self.conn:
                self.db = self.conn[self.db_name]
                self.cursor = self.db[self.table_name]
                (start,end) = self.five_time()
                #处理5分钟前的数据,基于域名的测试
                for obj in self.cursor.find({"time":{"$gte": start, "$lt": end},"domain":"192.168.60.77"}):
                    self.count_ng1(obj)
                    self.count_be1(obj)
                    self.count_total(self.host)
                    self.backtime_total(obj)
                    self.bodysize_total(obj)
                    self.count_fxx(obj)
                    self.count_ng3(obj)
                    self.count_too(obj)
                    self.count_sxx(obj)
                    self.nginxtime_total(obj)
                    self.count_be3(obj)
                
                #插入详情数据库
                self.insert_detail("detail")
        except Exception,e:
            print e
        finally:
            self.conn.close()
            
    def insert_detail(self,tablename):
        #插入数据供分析
        self.db[tablename].save({"bodysize_total":self.total_bodysize,
                                 "domain":"192.168.60.77",
                                 "ng1_count":self.ng1_count,
                                 "be1_count":self.be1_count,
                                 "total_count":self.total_count,
                                 "backtime_total":self.total_backtime,
                                 "bodysize_total":self.total_bodysize,
                                 "xx4_count":self.fxx_count,
                                 "time":datetime.datetime.utcnow(),
                                 "ng3_count":self.ng3_count,
                                 "c200_count":self.too_count,
                                 "xx5_count":self.sxx_count,
                                 "ngxtime_total":self.total_nginxtime,
                                 "be3_count":self.be1_count
                                 })
    def Command(self,argv):
        try:
            conn = pymongo.Connection(self.host,self.port)
            if conn:
                self.db = conn["nginx"]
                self.cursor = self.db["detail"]
                for obj in self.cursor.find({},{"total_count":1}).sort([("_id",-1)]).limit(1):
                        count_total = obj["total_count"]
                print count_total
                #域名的总请求数
                if argv == "total_count":
                    print count_total
                #2XX率
                elif argv == "c200_count":
                    for obj in self.cursor.find({},{"c200_count":1}).sort([("_id",-1)]).limit(1):
                        ctwo_count = obj["c200_count"]
                    print round((float(ctwo_count)*100)/count_total,2)
                #elif argv == "xx4_count":
                    #for obj in self.cursor.find({},{"c200_count":1}).sort([("_id",-1)]).limit(1):
        except Exception,e:
            print e
                
        
        
        
        
        
if __name__ == '__main__':   
    Conn = MongoConnection()
    Conn.conn()
    Conn.Command("c200_count")

    
