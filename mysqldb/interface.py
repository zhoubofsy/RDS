#!/usr/bin/env python
#coding:utf-8

import mysql

# exec sql & command by root
def execute_by_root(cmd=""):
    return mysql_execute('root', cmd)

# exec command by monitor
def execute_by_monitor(cmd=""):
    return mysql_execute('monitor', cmd)

def mysql_execute(user_type, cmd=""):
    result_cmd = None
    if cmd == None or cmd == "":
        return result_cmd
    
    # Connnect mysqldb by monitor
    connector = mysql.mysql_get_connector(user_type)
    if connector != None:
        # Execute command
        result_cmd = connector.execute(cmd)
        connector.disconnect()

    return result_cmd

#debug:
if __name__=="__main__":
    import pdb
    pdb.set_trace()
    ret = ""
    try:
        ret = execute_by_monitor("show grantss")
    except Exception as e:
        print e
    print ret
    exit(0)
