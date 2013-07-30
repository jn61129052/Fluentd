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
        
    #��XX��ֵ    
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

    #��XX�ٷֱ�    
    def lbdetail_persent(self,command):
        return round((float(self.connection(command))*100)/self.connection("total_count"),2)
    
    #��XXƽ��ֵ
    def lbdetail_average(self,command):
        return float(self.connection(command)/self.connection("total_count"))

    #ִ��
    def fluentd_nginx(self):
        
        #��������������
        if self.command == "total_count":
            print self.connection("total_count")
            
        #2XX��
        elif self.command == "c200_count_persent":
            print self.lbdetail_persent("c200_count")
        
        #4XX��
        elif self.command == "xx4_count_persent":
            print self.lbdetail_persent("xx4_count")
        
        #4XX��
        elif self.command == "xx4_count":
            print self.connection("xx4_count")
            
        #5xx��
        elif self.command == "xx5_count_persent":
            print self.lbdetail_persent("xx5_count")
            
        #5XX��
        elif self.command == "xx5_count":
            print self.connection("xx5_count")
            
        #ƽ����Ӧʱ��
        elif self.command == "nginxtime_average":
            print self.lbdetail_average("ngxtime_total")
        
        #�����Ӧ����1��ı���
        elif self.command == "be1_count_persent":
            print self.lbdetail_persent("be1_count")
        
        #�����Ӧ����3��ı���
        elif self.command == "be3_count_persent":
            print self.lbdetail_persent("be3_count")
            
        #���ƽ����Ӧʱ��
        elif self.command == "backtime_total_average":
            print self.lbdetail_average("backtime_total")
            
        #bodysizeƽ����С
        elif self.command == "bodysize_total_average":
            print self.lbdetail_average("bodysize_total")
        
        #nginx��Ӧ����1��ı���
        elif self.command == "ng1_count_persent":
            print self.lbdetail_persent("ng1_count")
        
        #nginx��Ӧ����3��ı���
        elif self.command == "ng3_count_persent":
            print self.lbdetail_persent("ng3_count")
            
if __name__ == "__main__":
        a = Analysis(sys.argv[1],"nginx","detail")
        a.fluentd_nginx()

            
        
        
    