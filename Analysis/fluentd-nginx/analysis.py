#-*- coding: gbk -*-
#coding=gbk 
#!/usr/bin/env python2.7
import pymongo
import sys
class Analysis(object):
    def __init__(self,command,db_name,table_name):
        self.command = command
        self.host = "192.168.60.77"
        self.port = 27017
        self.db_name = db_name
        self.table_name = table_name
        
    #求XX的值    
    def connection(self,command):
        try:
            self.conn = pymongo.Connection(self.host,self.port)
            if self.conn:
                self.db = self.conn[self.db_name]
                self.cursor = self.db[self.table_name]
                for obj in self.cursor.find({},{command:1}).sort([("_id",-1)]).limit(1):
                    count = obj[command]
                return count
        except Exception,e:
            print e

    #求XX百分比    
    def lbdetail_persent(self,command):
        return round((float(self.connection(command))*100)/self.connection("total_count"),2)
    
    #求XX平均值
    def lbdetail_average(self,command):
        return float(self.connection(command)/self.connection("total_count"))

    #执行
    def fluentd_nginx(self):
        
        #域名的总请求数
        if self.command == "total_count":
            print self.connection("total_count")
            
        #2XX率
        elif self.command == "c200_count_persent":
            print self.lbdetail_persent("c200_count")
        
        #4XX率
        elif self.command == "xx4_count_persent":
            print self.lbdetail_persent("xx4_count")
        
        #4XX数
        elif self.command == "xx4_count":
            print self.connection("xx4_count")
            
        #5xx率
        elif self.command == "xx5_count_persent":
            print self.lbdetail_persent("xx5_count")
            
        #5XX数
        elif self.command == "xx5_count":
            print self.connection("xx5_count")
            
        #平均响应时间
        elif self.command == "nginxtime_average":
            print self.lbdetail_average("ngxtime_total")
        
        #后端响应超过1秒的比率
        elif self.command == "be1_count_persent":
            print self.lbdetail_persent("be1_count")
        
        #后端响应超过3秒的比率
        elif self.command == "be3_count_persent":
            print self.lbdetail_persent("be3_count")
            
        #后端平均响应时间
        elif self.command == "backtime_total_average":
            print self.lbdetail_average("backtime_total")
            
        #bodysize平均大小
        elif self.command == "bodysize_total_average":
            print self.lbdetail_average("bodysize_total")
        
        #nginx响应大于1秒的比率
        elif self.command == "ng1_count_persent":
            print self.lbdetail_persent("ng1_count")
        
        #nginx响应大于3秒的比率
        elif self.command == "ng3_count_persent":
            print self.lbdetail_persent("ng3_count")
            
if __name__ == "__main__":
        a = Analysis(sys.argv[1],"nginx","detail")
        a.fluentd_nginx()

            
        
        
    