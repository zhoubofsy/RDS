#!/usr/bin/env python
#coding:utf-8

PRIV_TYPE_NONE = 'NONE'
PRIV_TYPE_RO = 'RO'
PRIV_TYPE_RW = 'RW'
PRIV_TYPE_ALL = 'ALL'

priv_map = {
    PRIV_TYPE_NONE : ['USAGE'],
    PRIV_TYPE_RO : ['SELECT','SHOW VIEW','CREATE ROUTINE','EXECUTE'],
    PRIV_TYPE_RW : ['CREATE','DROP','LOCK TABLES','REFERENCES','EVENT','ALTER','DELETE','INDEX','INSERT','SELECT','UPDATE','CREATE TEMPORARY TABLES','TRIGGER','CREATE VIEW','SHOW VIEW','ALTER ROUTINE','CREATE ROUTINE','EXECUTE'],
    PRIV_TYPE_ALL : ['ALL PRIVILEGES'],
}

def get_privs(priv_type):
    if None == priv_type or "" == priv_type or None == priv_map.get(priv_type):
        priv_type = PRIV_TYPE_NONE
    return priv_map[priv_type]

def priv_dump(priv_type):
    if priv_type == None or priv_type == "":
        return None
    priv_str = ""
    privs_list = get_privs(priv_type)
    for priv in privs_list:
        priv_str = priv_str + priv
        if priv != privs_list[len(privs_list) - 1]:
            priv_str = priv_str + ','

    if priv_str == "":
        priv_str = None
    return priv_str

def analyse_privs(privs_list):
    # Todo...
    # return PRIV_TYPE_*
    if privs_list == None or len(privs_list) <= 0:
        return None
    ret_type = PRIV_TYPE_NONE
    for (priv_type,privs) in priv_map.items():
        if priv_type == PRIV_TYPE_NONE:
            if len(set(privs_list) & set(privs)) == 1:
                ret_type = priv_type
                break
        elif priv_type == PRIV_TYPE_RO:
            if len(set(privs_list) - set(privs)) == 0:
                ret_type = priv_type
                break
        elif priv_type == PRIV_TYPE_RW:
            write_only_set = set(get_privs(PRIV_TYPE_RW)) - set(get_privs(PRIV_TYPE_RO))
            if len(set(privs_list) & write_only_set) > 0:
                ret_type = priv_type
                break
        elif priv_type == PRIV_TYPE_ALL:
            if len(set(privs_list) & set(privs)) == 1:
                ret_type = PRIV_TYPE_RW
                break
        else:
            assert False
    return ret_type
#debug
if __name__=="__main__":
    import pdb
    pdb.set_trace()
    input = ["USAGE"]
    print analyse_privs(input)
    input = ["INSERT"]
    print analyse_privs(input)
    input = ['INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'REFERENCES', 'INDEX', 'ALTER', 'CREATE TEMPORARY TABLES', 'LOCK TABLES', 'EXECUTE', 'CREATE VIEW', 'SHOW VIEW', 'CREATE ROUTINE', 'ALTER ROUTINE', 'EVENT', 'TRIGGER']
    print analyse_privs(input)
    input = ["SELECT","EXECUTE"]
    print analyse_privs(input)

