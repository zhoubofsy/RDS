#!/usr/bin/env python
#coding:utf-8

import time
def show_Threads():
    try :
        res = execute_by_monitor("show status like 'Thread_%'")
    except e:
        ret = {}
        ret['type'] = e[0]
        ret['code'] = e[1]
        ret['description'] = e[2]
        ret['Err_moudle'] = 'show_Threads'
        return ret
    ret = {}
    for items in res:
        if items[0] == 'Threads_connected' or items[0] == 'Threads_connected' :
            ret[ items[0] ] = items[1]
        else :
            pass
    return ret

def calc_temp():
    try :
        res = execute_by_monitor("show status like 'Created_tmp%_tables'")
    except e:
        ret = {}
        ret['type'] = e[0]
        ret['code'] = e[1]
        ret['description'] = e[2]
        ret['Err_moudle'] = 'calc_temp'
        return ret
    ret = {}
    for items in res:
        if items[0] == 'Created_tmp_tables' or items[0] == 'Created_tmp_disk_tables' :
            ret[ items[0] ] = items[1]
        else :
            pass
        ret['Temp_Usage'] = ret['Created_tmp_tables']/ret['Created_tmp_disk_tables']
        del ret['Created_tmp_tables']
        del ret['Created_tmp_disk_tables']
    return ret

def get_QPS():
    res = execute_by_monitor("show status like 'Queries'")
    ret = {}
    for items in res:
        if items[0] == 'Queries' :
            ret[ items[0] ] = items[1]
        else :
            pass
    return ret

def get_TPS():
    res = execute_by_monitor("show status like 'Com%'")
    ret = {}
    for items in res:
        if items[0] == 'Com_commit' or items[0] == 'Com_rollback' :
            ret[ items[0] ] = items[1]
        else :
            pass
    return ret

def calc_QPS(time_int = 1):
    ret = {}
    time_spot = []
    try :
        time_spot[0] += get_QPS()
        time.sleep(time_int)
        time_spot[1] = get_QPS()
    except e :
        ret = {}
        ret['type'] = e[0]
        ret['code'] = e[1]
        ret['description'] = e[2]
        ret['Err_moudle'] = 'calc_QPS'
        return ret
    if 'Queries' in time_spot[0] and 'Queries' in time_spot[1] :
        ret['QPS'] = (time_spot[1]['Queries'] - time_spot[0]['Queries'] ) / time_int
    return ret

def calc_TPS(time_int = 1):
    ret = {}
    time_spot = []
    try :
        time_spot[0] += get_TPS()
        time.sleep(time_int)
        time_spot[1] = get_TPS()
    except e :
        ret = {}
        ret['type'] = e[0]
        ret['code'] = e[1]
        ret['description'] = e[2]
        ret['Err_moudle'] = 'calc_TPS'
        return ret
    if 'Com_commit' in time_spot[0] and 'Com_commit' in time_spot[1] and 'Com_rollback' in time_spot[0] and 'Com_rollback' in time_spot[1]:
        ret['TPS'] = (time_spot[1]['Com_commit'] - time_spot[0]['Com_commit'] + time_spot[1]['Com_rollback'] - time_spot[0]['Com_rollback']) / time_int
    return ret

def show_COMDML():
    try :
        res = execute_by_monitor("show status like 'Com%'")
    except e:
        ret = {}
        ret['type'] = e[0]
        ret['code'] = e[1]
        ret['description'] = e[2]
        ret['Err_moudle'] = 'show_COMDML'
        return ret
    if res[0][0] == 'Error' :
        return None
    ret = {}
    for items in res:
        if items[0] == 'Com_insert' or items[0] == 'Com_insert_select' or items[0] == 'Com_replace' or items[0] == 'Com_replace_select' :
            ret[ items[0] ] = items[1]
        elif items[0] == 'Com_select' or items[0] == 'Com_delete' or items[0] == 'Com_delete_multi' or items[0] == 'Com_update' or items[0] == 'Com_update_multi' :
            ret[ items[0] ] = items[1]
        else :
            pass
    return ret
