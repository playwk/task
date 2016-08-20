# Auther: ZhengZhong,Jiang


import os
import json
from core import initialize
from core import atm_cardmgt
from core import atm_user
from conf import settings
import log


msg = """
1.登录
2.注册
3.退出
"""


def login():
    while True:
        user_type = input("是否是管理员：(y/n) ").strip()
        if user_type  == 'y':
            user_name = input("用户名：").strip()
            data = json.load(open("%s/user.db" % settings.DB_DIR, 'r'))
            if user_name in data:
                user_pass = input("密码：")
                if user_pass == data[user_name]:
                    atm_cardmgt.main()
                else:
                    print("认证失败！")
            else:
                print("用户名无效！")
        elif user_type == 'n':
            cardno = input("卡号：").strip()
            data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
            if cardno in data:
                user_pass = input("密码：")
                if user_pass == data[cardno][2]:
                    atm_user.main(cardno)
                else:
                    print("认证失败！")
            else:
                print("卡号不存在！")




def regisetr():
    while True:
        data = json.load(open("%s/user.db" % settings.DB_DIR, 'r'))
        user_name = input("用户名：").strip()
        if user_name in data:
            print("用户名已存在！")
            continue
        else:
            user_pass = input("密 码：")
            data[user_name] = user_pass
            json.dump(data, open("%s/user.db"  % settings.DB_DIR, 'w'))
            print("注册成功！")
            break


def main():
    initialize.initialize_atm()
    while True:
        print("ATM+ 信用卡管理系统".center(22, '-'))
        print(msg)
        user_input = input("请输入：").strip()
        if user_input == '1':
            login()
        elif user_input == '2':
            regisetr()
        elif user_input == '3':
            exit()
        else:
            print("选择无效！")

