#!/usr/bin/env python
#coding:utf-8

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from request import parse_formvars
    from rds.dbmng import *
    from rds.log import *
    from rds.authmng import *
    import rds.rds_err as rdserr
    import base_mng
else:
    from request import parse_formvars
    from rds.dbmng import *
    from rds.log import *
    from rds.authmng import *
    import rds.rds_err as rdserr
    import base_mng

def do_get_request(env):
    # params
    islist = False
    fields = parse_formvars(env)
    if fields.has_key('list'):
        islist = True
    else:
        code = rdserr.CODE_ERROR_PARAMS
        dbs = ''
    
    if islist:
        # list databases:
        try:
            dbs = list_dbs()
            code = rdserr.CODE_SUCCESS
        except Exception, e:
            log.error("[db mng][do_get_request] Exception %s"%(e))
            code = rdserr.map_exception_to_code(int(e[0]))
            dbs = '' 
    ret = {u'code':code,u'str':rdserr.get_str_by_code(code),u'body':dbs}
    return ret

def do_post_request(env):
    # params:
    fields = parse_formvars(env)
    if fields.has_key('nmDB') and fields.has_key('defCharacterSetDB'):
        name = fields['nmDB']
        charset = fields['defCharacterSetDB']
        if name == None or name.strip() == "" or charset == None or charset.strip() == "":
            code = rdserr.CODE_ERROR_PARAMS
        else:
            try:
                created_success = False
                # judge db exist
                if judge_db_exist(name):
                    code = rdserr.CODE_SUCCESS_DB_EXISTS
                # judge charset valid
                elif not judge_charset_valid(charset):
                    code = rdserr.CODE_ERROR_DB_CHARSET
                else:
                    # create db
                    if 0 == create_db(name,charset):
                        created_success = True
                        code = rdserr.CODE_SUCCESS
                # grant to dba
                if judge_db_exist(name):
                    #Todo...grant db to dba
                    grant('dba',name,'RW')
                    pass
                else:
                    code = rdserr.CODE_ERROR_DB_CREATE
            except Exception, e:
                log.error("[db mng][do_post_request] Exception %s"%(e))
                code = rdserr.map_exception_to_code(int(e[0]))
                if created_success:
                    try:
                        dbmng_drop_db(name)
                    except Exception, e:
                        log.warning("[db mng][do_post_request] Exception Drop db %s"%(e))
    else:
        code = rdserr.CODE_ERROR_PARAMS
    ret = {u'code':code,u'str':rdserr.get_str_by_code(code),u'body':u''}
    return ret

def do_delete_request(env):
    # params:
    name = None
    fields = parse_formvars(env)
    if fields.has_key('nmDB'):
        name = fields['nmDB']
    if name == None or name.strip() == "":
        code = rdserr.CODE_ERROR_PARAMS  
    else:
        try:
            # revoke from dba
            if judge_db_exist(name):
                # Todo...
                pass
            if 0 == drop_db(name):
                code = rdserr.CODE_SUCCESS
        except Exception, e:
            log.error("[db mng][do_delete_request] Exception %s"%(e))
            code = rdserr.map_exception_to_code(int(e[0]))
    ret = {u'code':code,u'str':rdserr.get_str_by_code(code),u'body':u''}
    return ret

class DBMng(base_mng.BaseMng):
    def process_get_request(self, env):
        ret_value = -1
        result = do_get_request(env)
        if result != None:
            self.set_response_header('200 OK', [('Content-Type','text/html')])
            self.set_response_body(result)
            ret_value = 0
        return ret_value

    def process_post_request(self,env):
        ret_value = -1
        result = do_post_request(env)
        if result != None:
            self.set_response_header('200 OK', [('Content-Type','text/html')])
            self.set_response_body(result)
            ret_value = 0
        return ret_value

    def process_delete_request(self,env):
        ret_value = -1
        result = do_delete_request(env)
        if result != None:
            self.set_response_header('200 OK', [('Content-Type','text/html')])
            self.set_response_body(result)
            ret_value = 0
        return ret_value
 
if __name__ == "__main__":
    import pdb
    pdb.set_trace()
    db_manager = DBMng()
    print db_manager
