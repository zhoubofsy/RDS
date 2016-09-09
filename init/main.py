#!/usr/bin/python
#coding:utf8

import pdb
import argparse
from scan_disk import auto_scan_disk
from prepare_fs import mkfs
from prepare_fs import mnt
from prepare_fs import is_mnt
from prepare_fs import set_fstab
from service_ctl import cmd_exec
from service_ctl import cmd_exec2
from service_ctl import service_start
from service_ctl import service_del
from service_ctl import service_add
#import sys
#sys.path.append('..')
from rds.log import *

def_mnt_point = '/store'
def_fs_type = 'ext4'
def_mysql_data_src = '/cs/mysql/data'

# startup:
def startup(device, mt_point = def_mnt_point, fs_type = def_fs_type, mysql_data_src = def_mysql_data_src):
    #pdb.set_trace()
    log.debug("[init rds][startup] entry")
    return 0
    ret = -1
    mounted = False
    fs = fs_type
    mount_point = mt_point
    data_src = mysql_data_src
    dev = device

    ## 1. Scan disks
    #disk = auto_scan_disk()
    #if disk != None and len(disk) >= 1:
    #    dev = disk[0]

    # 2. Format disk & mount
    if dev != "":
        if (not is_mnt(mount_point)): 
            cmd_exec("mkdir -p " + mount_point, False)
            if 0 == mkfs(fs,dev) and 0 == mnt(fs,dev,mount_point):
                # 3. Modify fstab
                set_fstab(fs,dev,mount_point)
                # 4. copy data_src to mount_point
                cmd_exec2("/bin/cp -r " + data_src + "/* " + mount_point + "/", True)
                # 5. rm -rvf /${mount_point}/lost+found
                cmd_exec2("/bin/rm -rvf "+ mount_point + "/lost+found", True)
                # 5. Remove rdsd service
                # 6. Add mysqld service
                #if 0 == service_del('rdsd') and 0 == service_add('mysqld'):
                if 0 == service_add('mysqld'):
                    # 7. Start mysqld service
                    ret = service_start('mysqld')
        else:
            ret = 0
    
    return ret
#main:
if __name__=="__main__":
    #pdb.set_trace()
    input_fs = def_fs_type
    input_dev = ""
    input_mnt = def_mnt_point
    input_src = def_mysql_data_src

    ret = startup(input_dev, input_mnt, input_fs, input_src)

    if ret == 0:
        exit(0)
    else:
        exit(1)
