#!/usr/bin/env python
#coding:utf-8

from request import parse_formvars
from rds.authmng import *
from rds.dbmng import *
from rds.log import *
import rds.rds_err as rdserr
import base_mng

def find_miss_dbs(dbs):
    #[miss db list...]
    miss_dbs = []
    for it_db in dbs:
        if not judge_db_exist(it_db):
            miss_dbs.append(it_db)
    return miss_dbs

def find_miss_users(users):
    #[miss user list...]
    miss_users = []
    return miss_users

def multi_grant(users, dbs, auth, finish_dbs = None, finish_users = None):
    for it_user in users:
        for it_db in dbs:
            if 0 == grant(it_user, it_db, auth) and finish_dbs != None:
                finish_dbs.append(it_db)
        if None != finish_users:
            finish_users.append(it_user) 
            finish_dbs = []
    return 0

def multi_revoke(users, dbs, finish_dbs = None, finish_users = None):
    for it_user in users:
        for it_db in dbs:
            if 0 == revoke(it_user, it_db) and finish_dbs != None:
                finish_dbs.append(it_db)
        if None != finish_users:
            finish_users.append(it_user) 
            finish_dbs = []
    return 0


def do_grant_operation(body):
    #{'code':code,'result':result}
    json_body = json.loads(body.strip())
    if dict != type(json_body) or (not json_body.has_key("users")) or (not json_body.has_key("dbs")) or (not json_body.has_key("auth")):
        code = rdserr.CODE_ERROR_PARAMS
        result = ""
    else:
        users = json_body['users']
        dbs = json_body['dbs']
        auth = json_body['auth']
        
        miss_dbs = find_miss_dbs(dbs)
        miss_users = find_miss_users(users)
        if len(miss_dbs) > 0:
            # Miss DB:
            code = rdserr.CODE_ERROR_DB_NOT_EXISTS
            result = miss_dbs
        elif len(miss_users) > 0:
            # Miss User:
            code = rdserr.CODE_ERROR_USER_NOT_EXISTS
            result = miss_users
        else:
            finish_dbs = []
            finish_users = []
            multi_grant(users,dbs,auth, finish_dbs, finish_users)
            # compare input & output length == 0 success
            if len(users) == len(finish_users) and len(dbs) == len(finish_dbs):
                code = rdserr.CODE_SUCCESS
                result = ""
            else:
                code = rdserr.CODE_ERROR_UNKNOW
                result = [finish_users,finish_dbs]
    ret = {'code':code,'result':result}
    return ret


def do_revoke_operation(body):
    #{'code':code,'result':result}
    json_body = json.loads(body.strip())
    if dict != type(json_body) or (not json_body.has_key("users")) or (not json_body.has_key("dbs")):
        code = rdserr.CODE_ERROR_PARAMS
        result = ""
    else:
        users = json_body['users']
        dbs = json_body['dbs']
        
        miss_dbs = find_miss_dbs(dbs)
        miss_users = find_miss_users(users)
        if len(miss_dbs) > 0:
            # Miss DB:
            code = rdserr.CODE_ERROR_DB_NOT_EXISTS
            result = miss_dbs
        elif len(miss_users) > 0:
            # Miss User:
            code = rdserr.CODE_ERROR_USER_NOT_EXISTS
            result = miss_users
        else:
            finish_dbs = []
            finish_users = []
            multi_revoke(users,dbs, finish_dbs, finish_users)
            # compare input & output length == 0 success
            if len(users) == len(finish_users) and len(dbs) == len(finish_dbs):
                code = rdserr.CODE_SUCCESS
                result = ""
            else:
                code = rdserr.CODE_ERROR_UNKNOW
                result = [finish_users,finish_dbs]
    ret = {'code':code,'result':result}
    return ret



def do_put_request(env):
    body = ""
    req_body = None
    # params: 
    fields = parse_formvars(env)
    if fields.has_key('grant') and None != env['wsgi.input']:
        req_body = env['wsgi.input'].read(int(env['CONTENT_LENGTH']))
        if req_body == None or req_body == "":
            code = rdserr.CODE_ERROR_PARAMS
        else:
            # grant operation:
            try:
                log.debug("--------here------------%s, %s"%(type(req_body),req_body))
                ret_data = do_grant_operation(req_body)
                code = ret_data['code']
                body = ret_data['result']
            except Exception, e:
                log.error("[auth mng][do_put_request] grant operation Exception %s"%(e))
                code = rdserr.map_exception_to_code(int(e[0]))
    elif fields.has_key('revoke') and None != env['wsgi.input']:
        req_body = env['wsgi.input'].read(int(env['CONTENT_LENGTH']))
        if req_body == None or req_body == "":
            code = rdserr.CODE_ERROR_PARAMS
        else:
            # revoke operation:
            try:
                ret_data = do_revoke_operation(req_body)
                code = ret_data['code']
                body = ret_data['result']
            except Exception, e:
                log.error("[auth mng][do_put_request] revoke operation Exception %s"%(e))
                code = rdserr.map_exception_to_code(int(e[0]))
    else:
        code = rdserr.CODE_ERROR_PARAMS
    ret = {u'code':code,u'str':rdserr.get_str_by_code(code),u'body':body}
    return ret


def do_get_request(env):
    body = ""
    fields = parse_formvars(env)
    if fields.has_key('byUser'):
        user = fields['byUser']
        try:
            body = get_priv_by_user(user)
            code = rdserr.CODE_SUCCESS
        except Exception, e:
            log.error("[auth mng][do_get_request] Exception %s"%(e))
            code = rdserr.map_exception_to_code(int(e[0]))
    else:
        code = rdserr.CODE_ERROR_PARAMS
    ret = {u'code':code,u'str':rdserr.get_str_by_code(code),u'body':body}
    return ret

class AuthMng(base_mng.BaseMng):
    def process_get_request(self,env):
        ret_value = -1
        result = do_get_request(env)
        if result != None:
            self.set_response_header('200 OK', [('Content-Type','text/html')])
            self.set_response_body(result)
            ret_value = 0
        return ret_value

    def process_put_request(self,env):
        ret_value = -1
        result = do_put_request(env)
        if result != None:
            self.set_response_header('200 OK', [('Content-Type','text/html')])
            self.set_response_body(result)
            ret_value = 0
        return ret_value

