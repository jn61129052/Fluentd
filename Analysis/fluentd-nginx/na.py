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
    
    def lbdetail_persent(self,command):
        return round((float(self.connection(command))*100)/self.connection("total_count"),2)
    
    def lbdetail_average(self,command):
        return float(self.connection(command)/self.connection("total_count"))

    def fluentd_nginx(self):
        
        if self.command == "total_count":
            print self.connection("total_count")
            
        elif self.command == "c200_count":
            print self.lbdetail_persent(self.command)
        
        elif self.command == "xx4_count":
            print self.lbdetail_persent(self.command)
            
        elif self.command == "xx5_count":
            print self.lbdetail_persent(self.command)
            
        elif self.command == "nginxtime":
            print self.lbdetail_average(self.command)
        
        elif self.command == "be1_count":
            print self.lbdetail_persent(self.command)

if __name__ == "__main__":
        a = Analysis(sys.argv[1],"nginx","detail")
        a.fluentd_nginx()
