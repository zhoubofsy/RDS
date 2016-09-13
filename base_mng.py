#!/usr/bin/env python
#coding:utf-8

from rds.log import *
import json


class BaseMng(object):
    def __init__(self):
        self.__env = None
        self.__start_response_header = None
        self.__code = None
        self.__content_type = None
        self.__method = None
        self.__resp_body = None

    def set_req_env(self,env, start_response):
        self.__env = env
        self.__start_response_header = start_response

    def set_response_body(self, resp_body):
        self.__resp_body = resp_body

    def get_response_body(self):
        return self.__resp_body
    
    def json_dump_response_body(self):
        resp_body = self.get_response_body()
        ret_body = None
        if dict == type(resp_body):
            json_rep_body = json.dumps(resp_body, ensure_ascii=False)
            ret_body = json_rep_body.encode('utf-8')
        elif str == type(resp_body):
            ret_body = resp_body
        else:
            ret_body = ""

        return ret_body

    def set_response_header(self,code, content_type):
        self.__code = code
        self.__content_type = content_type
    def get_response_header_code(self):
        return self.__code
    def get_response_header_ctype(self):
        return self.__content_type
    
    def start_resp(self):
        code = self.get_response_header_code()
        content_type = self.get_response_header_ctype()

        if code == None or code == "":
            code = '200 OK'
        if content_type == None or content_type == "":
            content_type = [('Content_Type','text/html')]

        self.__start_response_header(code, content_type)

    def __method_not_allow(self):
        self.set_response_header('405 OK', [('Content-Type','text/html')])
        self.set_response_body("Method Not Allowed")
        
    def process_get_request(self, env):
        self.__method_not_allow()

    def process_put_request(self, env):
        self.__method_not_allow()
    
    def process_post_request(self, env):
        self.__method_not_allow()

    def process_delete_request(self, env):
        self.__method_not_allow()

    def entry(self,env, start_response):
        log.debug("[entry] environ %s"%(env))
        self.set_req_env(env,start_response)
        resp_body = ""

        if env.has_key('REQUEST_METHOD'):
            self.__method = env['REQUEST_METHOD']
        
        if self.__method == 'GET':
            self.process_get_request(env)
        elif self.__method == 'POST':
            self.process_post_request(env)
        elif self.__method == 'DELETE':
            self.process_delete_request(env)
        elif self.__method == 'PUT':
            self.process_put_request(env)
        else:
            self.__method_not_allow()
        self.start_resp()
        resp_body = self.json_dump_response_body()
        log.debug("[entry] response %s"%(resp_body))
        return [resp_body]

