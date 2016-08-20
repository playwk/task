#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5

"""
MyFtp服务器后台管理程序，用于添加用户，删除用户、修改用户密码和磁盘配额。
"""
import os
import json
import hashlib
import shutil
from conf import settings


def create_user():
    """
    添加用户
    :return:
    """
    if not os.path.exists(settings.USER_FILE):
        f = open(settings.USER_FILE, "w")
        f.close()
        user_dict = {}
    else:
        if os.stat(settings.USER_FILE).st_size == 0:
            user_dict = {}
        else:
            with open(settings.USER_FILE) as f:
                user_dict = json.load(f)
    while True:
        user_name = input("请输入用户的名字：  ").strip()
        if not user_name:
            print("名字不能为空！")
            continue
        if user_name in user_dict:
            print("该用户已经存在,请重新输入！")
            continue
        name = user_name
        break
    while True:
        password_1 = input('请输入密码： ').strip()
        if not password_1:
            print('密码不能为空！')
            continue
        password_2 = input('请再次输入密码： ').strip()
        if password_1 != password_2:
            print('您两次输入的密码不同，请重新输入！')
            continue
        hash_obj = hashlib.md5()
        hash_obj.update(bytes(password_1, encoding="utf-8"))
        password = hash_obj.hexdigest()
        break
    while True:
        quota_input = input("请输入用户的磁盘配额(GB）：  ").strip()
        if not quota_input:
            print("配额不能为空或小于0！")
            continue
        quota = quota_input
        break
    temp_dict = {
        "password": password,
        "quota": quota,
    }
    user_dict[name] = temp_dict
    with open(settings.USER_FILE, "w") as w:
        json.dump(user_dict, w)
    # 创建用户的家目录
    user_home = os.path.join(settings.USER_HOME_DIR, name)
    os.mkdir(user_home)
    print("用户【%s】创建成功" % name)


def change_password():
    """
    修改用户密码
    :return:
    """
    if not os.path.exists(settings.USER_FILE):
        print("当前没有任何用户！")
        return
    else:
        if os.stat(settings.USER_FILE).st_size == 0:
            print("当前没有任何用户！")
            return
        else:
            with open(settings.USER_FILE) as f:
                user_dict = json.load(f)
    while True:
        user_name = input("请输入要变更密码的用户的名字：  ").strip()
        if not user_name:
            print("名字不能为空！")
            continue
        if user_name not in user_dict:
            print("该用户不存在,请重新输入！")
            continue
        name = user_name
        break
    while True:
        password_1 = input('请输入新的密码： ').strip()
        if not password_1:
            print('密码不能为空！')
            continue
        password_2 = input('请再次输入密码： ').strip()
        if password_1 != password_2:
            print('您两次输入的密码不同，请重新输入！')
            continue
        # 密码使用MD5加密
        hash_obj = hashlib.md5()
        hash_obj.update(bytes(password_1, encoding="utf-8"))
        password = hash_obj.hexdigest()
        break
    user_dict[name]["password"] = password
    with open(settings.USER_FILE, "w") as w:
        json.dump(user_dict, w)
    print('【\033[32;0m密码修改成功，请注意保存！\033[0m】')


def change_quota():
    """
    修改用户磁盘限额
    :return:
    """
    if not os.path.exists(settings.USER_FILE):
        print("当前没有任何用户！")
        return
    else:
        if os.stat(settings.USER_FILE).st_size == 0:
            print("当前没有任何用户！")
            return
        else:
            with open(settings.USER_FILE) as f:
                user_dict = json.load(f)
    while True:
        user_name = input("请输入要变更配额的用户的名字：  ").strip()
        if not user_name:
            print("名字不能为空！")
            continue
        if user_name not in user_dict:
            print("该用户不存在,请重新输入！")
            continue
        name = user_name
        break
    while True:
        quota_limit = input('请输入新的配额： ').strip()
        if not quota_limit:
            print('配额不能为空或小于0！')
            continue
        quota = quota_limit
        break
    user_dict[name]["quota"] = quota
    with open(settings.USER_FILE, "w") as w:
        json.dump(user_dict, w)
    print('【\033[32;0m配额修改成功，当前磁盘配额为%sG！\033[0m】'% quota)


def del_user():
    """
    删除某个用户
    :return:
    """
    if not os.path.exists(settings.USER_FILE):
        print("当前没有任何用户！")
        return
    else:
        if os.stat(settings.USER_FILE).st_size == 0:
            print("当前没有任何用户！")
            return
        else:
            with open(settings.USER_FILE) as f:
                user_dict = json.load(f)
    while True:
        user_name = input("请输入要删除的用户的名字：  ").strip()
        if not user_name:
            print("名字不能为空！")
            continue
        if user_name not in user_dict:
            print("该账户不存在,请重新输入！")
            continue
        name = user_name
        break
    del user_dict[name]
    with open(settings.USER_FILE, "w") as w:
        json.dump(user_dict, w)
    user_home = os.path.join(settings.USER_HOME_DIR, name)
    # 使用shutil模块的remtree方法，删除用户家目录
    shutil.rmtree(user_home)
    print("用户【%s】删除成功" % name)


def system_exit():
    exit("退出系统，再见！")


def main():
    menu_dict = {
        "1": create_user,
        "2": change_password,
        "3": change_quota,
        "4": del_user,
        "5": system_exit
    }
    while True:
        print("""___________________
MyFtp后台管理系统
-------------------
【1】     创建用户
【2】     修改密码
【3】     修改配额
【4】     删除用户
【5】     退出系统
-------------------""")
        choice = input("请按数字进行选择：  ").strip()
        if choice in menu_dict:
            menu_dict[choice]()
        else:
            print("无效的选择！")
