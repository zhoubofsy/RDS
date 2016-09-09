#!/usr/bin/env python
#coding:utf-8

#debug
if __name__=="__main__":
    import sys
    sys.path.append("..")
    from mysqldb import *
    from log import *
    import pdb
else:
    from rds.mysqldb import *
    from rds.log import *
import parse_grants_info as parse
import privs_info as privs_info

def authmng_grant(user,db,auth):
    # Single grant
    ret = -1
    if user == None or user == "" or db == None or db == ""  or auth == None or auth == "":
        return ret
    privs = privs_info.priv_dump(auth)
    cmd_grant = "grant " + privs + " on " + db.strip() + ".* to " + user.strip()
    try:
        ret_data = execute_by_root(cmd_grant)
        if len(ret_data) == 0:
            ret = 0
    except Exception, e:
        log.warning("[auth mng][authmng_grant] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
        
    return ret

def authmng_revoke(user,db):
    # Single revoke
    ret = -1
    if user == None or user == "" or db == None or db == "":
        return ret
    privs = 'ALL'
    cmd_revoke = "revoke " + privs + " on " + db.strip() + ".* from " + user.strip()
    try:
        ret_data = execute_by_root(cmd_revoke)
        if len(ret_data) == 0:
            ret = 0
    except Exception, e:
        log.warning("[auth mng][authmng_revoke] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    return ret

def collect_grants(collector, grant):
    if collector == None or grant == None or len(grant) <= 0:
        return False
    (key,value) = grant.items()[0]
    if key == '*' and value == privs_info.PRIV_TYPE_NONE:
        return True
    if len(collector) == 0:
        collector.append(grant)
    else:
        bupdate = False
        for item in collector:
            (it_key,it_value) = item.items()[0]
            if it_key == key:
                if privs_info.PRIV_TYPE_RW == value:
                    item[it_key] = value
                    bupdate = True
                    break
                elif privs_info.PRIV_TYPE_NONE == it_value and value != it_value:
                    item[it_key] = value
                    bupdate = True
                    break
        if not bupdate:
            collector.append(grant) 
    return True

def authmng_get_priv_by_user(user):
    #[{'db name':'RO'/'RW'},...]
    ret = []
    if user == None or user == "":
        return ret
    cmd_show_grants = "show grants for " + user
    try:
        ret_data = execute_by_root(cmd_show_grants)
        ret = []
        for item in ret_data:
            grants = parse.parse_grants(item[0])
            priv_type = privs_info.analyse_privs(grants['privs'])
            tmp = {grants['db']:priv_type}
            collect_grants(ret,tmp)
    except Exception, e:
        log.warning("[auth mng][authmng_get_priv_by_user] Exception %s"%(e))
        excep_data = e[0][0]
        excep_code = excep_data[1]
        raise Exception(excep_code)
    return ret


#debug
if __name__=="__main__":
    #Todo...
    pdb.set_trace()
    #print authmng_get_priv_by_user('abc_tmp')
    print authmng_grant('abc_tmp','abc_db3','RW')
    print authmng_get_priv_by_user('abc_tmp')
    print authmng_revoke('abc_tmp','abc_db3')
    print authmng_get_priv_by_user('abc_tmp')

