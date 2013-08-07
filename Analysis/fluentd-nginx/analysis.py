#-*- coding: gbk -*-
#coding=gbk 
#!/usr/bin/env python2.7
import pymongo
import sys

#hostname,command

class Analysis(object):
    def __init__(self,hostname,domain,command):
        self.command = command
        #MongoDB Center
        self.host = "192.168.60.191" 
        self.port = 27017
        #self.domain = domain
        self.hostname = hostname
        self.domain = domain
        self.db_name = self.hostname
        self.table_name = "lq_detail"
        
    #XX count
    def connection(self,command):
        try:
            self.conn = pymongo.Connection(self.host,self.port)
            if self.conn:
                self.db = self.conn[self.db_name]
                self.cursor = self.db[self.table_name]
                for obj in self.cursor.find({"domain":self.domain},{command:1}).sort([("_id",-1)]).limit(1):
                    count = obj[command]
                return count
        except Exception,e:
            print e
        finally:
            self.conn.close()

    #XX PER
    def lbdetail_persent(self,command):
        if self.connection("total_count") == 0 :
            return 0
        else:
            return round((float(self.connection(command))*100)/self.connection("total_count"),2)
    
    #XX AVE
    def lbdetail_average(self,command):
        if self.connection("total_count") == 0 :
            return 0
        else:
            return float(self.connection(command)/self.connection("total_count"))

    #excute
    def fluentd_nginx(self):
        
        if self.command == "total_count":
            print self.connection("total_count")
            
        #2XX per
        elif self.command == "c200_count_persent":
            print self.lbdetail_persent("c200_count")
        
        #4XX per
        elif self.command == "xx4_count_persent":
            print self.lbdetail_persent("xx4_count")
        
        #4XX count
        elif self.command == "xx4_count":
            print self.connection("xx4_count")
            
        #5xx per
        elif self.command == "xx5_count_persent":
            print self.lbdetail_persent("xx5_count")
            
        #5XX count
        elif self.command == "xx5_count":
            print self.connection("xx5_count")
            
        #nginx ave
        elif self.command == "nginxtime_average":
            print self.lbdetail_average("nginxtime_total")
        
        #backtime>1 per
        elif self.command == "be1_count_persent":
            print self.lbdetail_persent("be1_count")
        
        #backtime>3 per
        elif self.command == "be3_count_persent":
            print self.lbdetail_persent("be3_count")
            
        #backtime ave
        elif self.command == "backtime_total_average":
            print self.lbdetail_average("backtime_total")
            
        #bodysize ave
        elif self.command == "bodysize_total_average":
            print self.lbdetail_average("bodysize_total")
        
        #nginx>1 per
        elif self.command == "ng1_count_persent":
            print self.lbdetail_persent("ng1_count")
        
        #nginx>3 per
        elif self.command == "ng3_count_persent":
            print self.lbdetail_persent("ng3_count")
            
if __name__ == "__main__":
        
        a = Analysis(sys.argv[1],sys.argv[2],sys.argv[3])
        #a = Analysis("ubuntu","192.168.60.191","xx4_count_persent")
        a.fluentd_nginx()

            
        
        
    