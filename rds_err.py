#!/usr/bin/env python
#coding:utf-8

from rds.log import *

CODE_SUCCESS = 200
CODE_SUCCESS_DB_EXISTS = 202
CODE_SUCCESS_USER_EXISTS = 203
CODE_ERROR_DB_CONNECT = 400
CODE_ERROR_DB_CHARSET = 401
CODE_ERROR_DB_CREATE = 402
CODE_ERROR_DB_DROP = 403
CODE_ERROR_USER_CREATE = 404
CODE_ERROR_USER_DROP = 405
CODE_ERROR_USER_NOT_EXISTS = 406
CODE_ERROR_PASSWORD = 407
CODE_ERROR_DB_NOT_EXISTS = 408
CODE_ERROR_MOUNTPOINT = 409
CODE_ERROR_ETH_NOT_EXISTS = 410
CODE_ERROR_DEV_NOT_EXISTS = 411
CODE_ERROR_PARAMS = 412
CODE_ERROR_UNKNOW = 500

codemap = {
    CODE_SUCCESS : u'成功',
    CODE_SUCCESS_DB_EXISTS : u'成功，数据库已存在',
    CODE_SUCCESS_USER_EXISTS : u'成功，用户已存在',
    CODE_ERROR_DB_CONNECT : u'失败，数据库连接失败',
    CODE_ERROR_DB_CHARSET : u'失败，字符集错误',
    CODE_ERROR_DB_CREATE : u'失败，数据库创建失败',
    CODE_ERROR_DB_DROP : u'失败，删除数据库失败',
    CODE_ERROR_USER_CREATE : u'失败，用户创建失败',
    CODE_ERROR_USER_DROP : u'失败，删除用户失败',
    CODE_ERROR_USER_NOT_EXISTS : u'失败，用户不存在',
    CODE_ERROR_PASSWORD : u'失败，重置密码失败',
    CODE_ERROR_DB_NOT_EXISTS : u'失败，数据库不存在',
    CODE_ERROR_MOUNTPOINT : u'失败，挂载点访问错误',
    CODE_ERROR_ETH_NOT_EXISTS : u'失败，网卡不存在',
    CODE_ERROR_DEV_NOT_EXISTS : u'失败，设备不存在',
    CODE_ERROR_PARAMS : u'失败，参数错误',
    CODE_ERROR_UNKNOW : u'未知错误'
}

exception_map = {
    2003 : CODE_ERROR_DB_CONNECT,
    1007 : CODE_SUCCESS_DB_EXISTS,
    1008 : CODE_ERROR_DB_DROP,
}

def map_exception_to_code(e):
    if None == exception_map.get(e):
        log.warning("[rds err][map_exception_to_code] unknow exception %d"%(e))
        return CODE_ERROR_UNKNOW
    return exception_map.get(e)

def get_str_by_code(code):
    if None == codemap.get(code):
        log.warning("[rds err][get_str_by_code] unknow code %d"%(code))
        return codemap.get(CODE_ERROR_UNKNOW)
    return codemap.get(code)

#debug:
if __name__=="__main__":
    #Todo...
    print get_errstr_by_code(407)

    print get_errstr_by_code(780)
