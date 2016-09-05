#!/usr/bin/python
#coding:utf8

import pdb
import argparse
import main

if __name__=="__main__":
    #pdb.set_trace()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fs", help="filesystem , default 'EXT4'", nargs='?', type=str, default=main.def_fs_type)
    parser.add_argument("device", help="block device", nargs=1, type=str)
    parser.add_argument("-m", "--mount", help="mount path, defautlt '/store'", nargs='?', type=str, default=main.def_mnt_point)
    parser.add_argument("-s", "--src", help="MySQL data path, default '/cs/mysql/data'", nargs='?', type=str, default=main.def_mysql_data_src)
    args = parser.parse_args()

    input_fs = def_fs_type
    input_dev = ""
    input_mnt = def_mnt_point
    input_src = def_mysql_data_src

    if args.fs != None and len(args.fs) > 0:
        input_fs = args.fs
    if len(args.device) > 0:
        input_dev = args.device[0]
    if args.mount != None and len(args.mount) > 0:
        input_mnt = args.mount.rstrip('/')
    if args.src != None and len(args.src) > 0:
        input_src = args.src.rstrip('/')

    ret = main.startup(input_dev, input_mnt, input_fs, input_src)

    if ret == 0:
        exit(0)
    else:
        exit(1)
