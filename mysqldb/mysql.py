#!/usr/bin/env python
#coding:utf-8

debug = False 
#debug = True
if debug:
    import sys
    sys.path.append("..")
    from log import *
    import MySQLdb as mdb
else:
    import MySQLdb as mdb
    from rds.log import *


def mysql_get_connector(user_type = 'root'):
    if user_type == None:
        return None
    if 'root' == user_type:
        # Connect by root
        mysql = MysqlConnectByRoot()
    elif 'monitor' == user_type:
        # Connect by monitor
        # mysql.connect('192.168.5.152','abc_tmp','')
        mysql = MysqlConnectByMonitor()
    else:
        mysql = None

    if mysql != None:
        mysql.connect()

    return mysql

class MysqlAdapter(object):
    def __init__(self):
        self.__db = None

    def connect(self,host="",user="",passwd="",db=""):
        try:
            self.__db = mdb.connect(host,user,passwd)
        except Exception, e:
            err_data = (('Error', e[0], e[1]),)
            log.error("[mysqldb][connect] %s"%(err_data))
            raise Exception(err_data)

    def execute(self,cmd=""):
        assert cmd != None and cmd != ""
        assert self.__db != None
        cursor = self.__db.cursor()
        try:
            cursor.execute(cmd)
        except:
            cursor.execute('show warnings')
            warn_data = cursor.fetchall()
            self.disconnect()
            log.error("[mysqldb][execute] %s"%(warn_data))
            raise Exception(warn_data)
        return cursor.fetchall()

    def disconnect(self):
        if self.__db != None:
            self.__db.close()

class MysqlConnectByMonitor(MysqlAdapter):
    def connect(self, host="localhost", user='monitor', passwd=''):
        super(MysqlConnectByMonitor,self).connect(host,user,passwd)

class MysqlConnectByRoot(MysqlAdapter):
    def connect(self, host='localhost', user='root',passwd=''):
        super(MysqlConnectByRoot,self).connect(host,user,passwd)
