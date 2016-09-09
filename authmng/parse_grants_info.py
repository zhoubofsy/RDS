#!/usr/bin/env python
#coding:utf-8


def parse_privs(privs):
    #['priv','priv'...'priv']
    if privs == None or privs == "":
        return None
    privs_list = privs.split(',')
    ret_privs = []
    for priv in privs_list:
        pos = priv.find('(')
        if pos < 0:
            priv_tmp = priv.strip()
        else:
            priv_tmp = priv[:pos].strip()
        ret_privs.append(priv_tmp)
    return ret_privs

def parse_db(db_orig):
    #db_name
    if db_orig == None or db_orig == "":
        return None
    db_split = db_orig.split('.')
    ret_db = db_split[0].strip().replace('`','')
    return ret_db

def parse_grants(grants_info):
    # Todo...
    #{'db':'db name',privs:[priv list]}
    str_grant = "GRANT "
    str_on = " ON "
    str_to = " TO "
    # get privs
    pos_grant = grants_info.find(str_grant)
    if pos_grant < 0:
        return None
    spos_privs = pos_grant + len(str_grant)
    pos_on = grants_info.find(str_on)
    if pos_on < 0:
        return None
    epos_privs = pos_on

    # get db name
    spos_db = pos_on + len(str_on)
    pos_to = grants_info.find(str_to)
    if pos_to < 0:
        return None
    epos_db = pos_to
    
    # parse grants info
    privs_list = None
    db = None
    if spos_privs < epos_privs and epos_privs < spos_db and spos_db < epos_db:
        privs_list = parse_privs(grants_info[spos_privs:epos_privs])
        db = parse_db(grants_info[spos_db:epos_db])
    if privs_list == None or db == None:
        return None
    
    ret = {'db':db,'privs':privs_list}
    return ret

#debug
if __name__=="__main__":
    import pdb
    pdb.set_trace()
    input = "GRANT USAGE ON *.* TO 'abc_tmp'@'%'"
    print parse_grants(input)
    input = "GRANT INSERT ON `abc`.* TO 'abc_tmp'@'%'"
    print parse_grants(input)
    input = "GRANT INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER ON `abc`.* TO 'abc_admin'@'%' WITH GRANT OPTION"
    print parse_grants(input)

    input = "GRANT UPDATE (age) ON `abc`.`a` TO 'abc_tmp'@'%'"
    print parse_grants(input)
