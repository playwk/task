#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

import libclass
import paramiko

msg = """
1.获取数据
2.设置数据
3.远程执行
"""


#主逻辑
while True:
    print(msg)
    choose = input(">>> ").strip()
    if choose == '1':
        tab_list = []
        for i, tab_name in enumerate(libclass.table_name, start=1):
            tab_list.append(tab_name[0])
            print('%s.%s' % (i, tab_name[0]))
        choose = input(">>> ").strip()
        if choose.isdigit() and int(choose) <= len(libclass.table_name):
            table = tab_list[int(choose)-1]
            print(table)
            obj = libclass.Manager(table)
            obj.select()
        else:
            print('choose invalid!')
    elif choose == '2':
        tab_list = []
        for i, tab_name in enumerate(libclass.table_name, start=1):
            tab_list.append(tab_name[0])
            print('%s.%s' % (i, tab_name[0]))
        choose = input(">>> ").strip()
        if choose.isdigit() and int(choose) <= len(libclass.table_name):
            table = tab_list[int(choose) - 1]
            print("""1.增加
2.删除"""
                  )
            obj = libclass.Manager(table)
            choose = input(">>> ").strip()
            if choose == '1':
                info_list = [obj.class_name, ]
                for i in obj.table_column:
                    if i != 'id':
                        inp = input("%s: " % i)
                        info_list.append(inp)
                obj.insert(info_list)
            elif choose == '2':
                #此处只支持表主键ID条件>某值的批量删除
                obj.select()
                for i in obj.table_column:
                    print(i)
                remove_condition = input("filter: ").strip()
                obj.remove(remove_condition)
        else:
            print('choose invalid!')
    elif choose == '3':
        choose = input("IP: ").strip()
        obj = libclass.Manager('host')
        obj.queryhost(choose)
        cmd = input('>>> ').strip()
        libclass.run_command(cmd, choose, obj.login_user, obj.login_pawd, obj.login_port)
    else:
        print('choose invalid!')



