#!/usr/bin/env python
#coding:utf-8

#debug 
if __name__=="__main__":
    import sys
    sys.path.append('..')
    from mysqldb import *
    from log import *
    import pdb
else:
    from rds.mysqldb import *
    from rds.log import *

def dbmng_list_dbs():
    #Todo...
    # list dbs, raise connect error exception
    list_cmd = "show databases"
    try:
        dbs_data = execute_by_root(list_cmd)
    except Exception, e:
        log.warning("[db mng][dbmng_list_dbs] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    # tuple to list
    dbs = []
    for item in dbs_data:
        dbs.append(item[0])
    return dbs

def dbmng_create_db(dbname,charset):
    # create db
    ret = -1
    create_cmd = "create database " + dbname.strip() + " character set " + charset.strip()
    try:
        ret_data = execute_by_root(create_cmd)
        ret = 0
    except Exception, e:
        log.warning("[db mng][dbmng_create_db] Create Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    return ret

def dbmng_drop_db(dbname):
    # drop db
    ret = -1
    drop_cmd = "drop database " + dbname.strip()
    try:
        ret_data = execute_by_root(drop_cmd)
        ret = 0
    except Exception, e:
        log.warning("[db mng][dbmng_drop_db] Drop Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    return ret

def dbmng_judge_db_exist(dbname):
    ret_exist = False
    judge_cmd = "show databases like '" + dbname.strip() +"'"
    try:
        ret_data = execute_by_root(judge_cmd)
    except Exception, e:
        log.warning("[db mng][dbmng_judge_db_exist] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    if len(ret_data) > 0 and ret_data[0][0] == dbname:
        ret_exist = True
    return ret_exist

def dbmng_judge_charset_valid(charset):
    ret_valid = False
    judge_cmd = "show character set like '" + charset.strip() + "'"
    try:
        ret_data = execute_by_root(judge_cmd)
    except Exception, e:
        log.warning("[db_mng][dbmng_judge_charset_valid] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    if len(ret_data) > 0 and ret_data[0][0] == charset:
        ret_valid = True
    return ret_valid

if __name__ == "__main__":
    pdb.set_trace()
    try:
        dbmng_create_db('dbmng_tst','utf8')
        print dbmng_list_dbs()
        dbmng_drop_db('dbmng_tst')
        print dbmng_list_dbs()
        print dbmng_judge_db_exist('dbmng_tst')
        print dbmng_judge_charset_valid('utf8')
    except Exception, e:
        print e
    print "--------- end ----------"

