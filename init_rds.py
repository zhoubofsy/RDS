#!/usr/bin/env python
#coding:utf-8

import os
from request import parse_formvars
from rds.init import *
from rds.log import *
import rds.rds_err as rdserr
import json

def is_valid_device(dev):
    if dev == None or dev == "":
        return False
    path = '/dev/'+dev.strip()
    if not os.path.exists(path):
        return False
    return True

def entry(environ, start_response):
    log.debug("[init rds][entry] environ %s"%(environ))
    # params:
    vol = ""
    fields = parse_formvars(environ)
    if fields.has_key('vol'):
        vol = fields['vol']
    if environ.has_key('REQUEST_METHOD'):
        method = environ['REQUEST_METHOD']

    if method == None or method != "PUT":
        start_response('405 OK', [('Content-Type','text/html')])
        ret_json = "Method Not Allowed"
    else:
        # check device:
        if not is_valid_device(vol):
            ret_code = rdserr.CODE_ERROR_DEV_NOT_EXISTS
        else:
            # init RDS:
            if 0 == init_rds(vol):
                # success:
                ret_code = rdserr.CODE_SUCCESS
            else:
                # failure:
                ret_code = rdserr.CODE_ERROR_UNKNOW
        # return json:
        str_code = rdserr.get_str_by_code(ret_code)
        ret_json = json.dumps({u'code':ret_code,u'str':str_code,u'body':u''},ensure_ascii=False)
        ret_json = ret_json.encode('utf-8')
        log.debug("[init rds][entry] result %s"%(ret_json))
        start_response('200 OK', [('Content-Type','text/html')])
    return [ret_json]


#debug:
if __name__=="__main__":
    #Todo...
    import pdb
    pdb.set_trace()
    init_rds('xvdb')
