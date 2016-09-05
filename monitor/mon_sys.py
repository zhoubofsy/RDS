#!/usr/bin/env python
#coding:utf-8

import time
import os
import pdb
import subprocess as proc

# volume size
# 计算挂载点容量大小
# 
def get_vol_size(path_mounted='/'):
    ret_hd = {}
    if path_mounted == None or path_mounted == "":
        return None
    disk = os.statvfs(path_mounted)
    ret_hd['available'] = disk.f_bsize * disk.f_bavail
    ret_hd['capacity'] = disk.f_bsize * disk.f_blocks
    ret_hd['used'] = ret_hd['capacity'] - ret_hd['available']
    return ret_hd


# cpu & mem usage
# CPU & MEMORY 占用率获取
# eg: ps aux | awk '/\/cs\/mysql\/bin\/mysqld /{print $3,$4}'
#
def get_cpu_mem_usage(path='/cs/mysql/bin/mysqld'):
    if path == None or path == "":
        return None
    process_path = path.replace('/','\\/')
    exec_cmd = "ps aux | awk '/" + process_path + " /{print $3,$4}'"
    p = proc.Popen(exec_cmd, stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT,shell=True)
    if 0 == p.wait():
        # success
        for line in p.stdout.readlines():
            ret_usage = line.strip().split(' ')
    else:
        # failure
        for line in p.stdout.readlines():
            print line
        ret_usage = None
    return ret_usage


# network receive & transmit
# 网络输入输出量
# cat /proc/net/dev | awk '$1 ~/^ens33:/{print $2,$10}'
# return : [receive,transmit]
# 
def get_network_rt(eth='lo'):
    if eth == None or eth == "":
        return None
    exec_cmd = "cat /proc/net/dev | awk '$1 ~/^" + eth + ":/{print $2,$10}'"
    p = proc.Popen(exec_cmd, stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT,shell=True)
    if 0 == p.wait():
        # success:
        tmp_rt = []
        for line in p.stdout.readlines():
            tmp_rt = line.strip().split(' ')
        if len(tmp_rt) == 2:
            ret_rt = []
            for item in tmp_rt:
                ret_rt.append(long(item))
        else:
            ret_rt = None
    else:
        # failure:
        for line in p.stdout.readlines():
            print line
        ret_rt = None
    return ret_rt


# network r&t usage
# 网络每分钟的输入输出量
#
def calc_rt_usage(eth='lo', sec=5):
    if sec <= 0:
        return None
    start_rt = get_network_rt(eth)
    # sleep
    time.sleep(sec)
    end_rt = get_network_rt(eth)

    if start_rt == None or end_rt == None:
        return None
    assert len(start_rt) == len(end_rt) and len(end_rt) > 0
    #ret_rt_usage = list((set(end_rt) - set(start_rt)) / sec)
    ret_rt_usage = []
    for i in range(0,len(end_rt)):
        ret_rt_usage.append((end_rt[i] - start_rt[i]) / sec)
    return ret_rt_usage

# IOPS
# 获取指定硬盘的OPS
# cat /proc/diskstats  | awk '/xvdc /{print $4,$8}'
# return : [read ops, write ops]
#
def get_iops(dev='xvdc'):
    if dev == None or dev == "":
        return None
    exec_cmd = "cat /proc/diskstats | awk '/" + dev + " /{print $4,$8}'"
    p = proc.Popen(exec_cmd,stdin=proc.PIPE,stdout=proc.PIPE,stderr=proc.STDOUT,shell=True)
    if 0 == p.wait():
        # success:
        tmp_ops = []
        for line in p.stdout.readlines():
            tmp_ops = line.strip().split(' ')
        if len(tmp_ops) == 2:
            ret_ops = []
            for item in tmp_ops:
                ret_ops.append(long(item))
        else:
            ret_ops = None
    else:
        # failure:
        for line in p.stdout.readlines():
            print line
        ret_ops = None
    return ret_ops

# Calc IOPS
# 计算IOPS
# 
def calc_iops(dev, sec=5):
    if sec <=0:
        return None
    start_iops = get_iops(dev)
    # sleep
    time.sleep(sec)
    end_iops = get_iops(dev)

    if start_iops == None or end_iops == None:
        return None
    assert len(start_iops) == len(end_iops) and len(end_iops) > 0
    ret_iops = []
    for i in range(0,len(end_iops)):
        ret_iops.append((end_iops[i] - start_iops[i])/sec)
    return ret_iops

if __name__=="__main__":
    # Testing:
    #pdb.set_trace()
    ret = get_vol_size()
    print ret
    #pdb.set_trace()
    ret = get_cpu_mem_usage('/usr/sbin/mysqld')
    print ret
    #pdb.set_trace()
    ret = calc_rt_usage('ens33')
    print ret
    ret = calc_iops('sda')
    print ret
