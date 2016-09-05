#!/usr/bin/env python
#coding:utf-8

import logging

def init():
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%d %b %Y %H:%M:%S',
            filename='/var/log/rds.log')

#debug
if __name__=="__main__":
    #Todo...
    init()
    logging.debug("Hello logging")
