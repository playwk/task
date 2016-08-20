# Auther: ZhengZhong,Jiang

import json
from conf import settings

msg = """
欢迎登录>>>
1.添加账户
2.注销账户
3.修改账户
4.冻结账户
"""

def account_add():
    """
    开卡操作
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    print("以 , 为分隔符，依次输入开卡卡号，卡片状态，卡片余额，卡片额度，支付密码，账单日期，还款日期，本期欠款")
    add_info = input(">>> ")
    card_info = add_info.split(',')
    if card_info[0] in data:
        print("该卡已存在！")
    else:
        data[card_info[0]] = [card_info[1], card_info[2], card_info[3], card_info[4], card_info[5], card_info[6]]
        json.dump(data, open("%s/card.db" % settings.DB_DIR, 'w'))
        print("开卡成功！")


def account_del():
    """
    销卡操作
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    user_input = input("输入销卡卡号：").strip()
    if user_input in data:
        data.remove(user_input)
        json.dump(data, open("%s/card.db" % settings.DB_DIR, 'w'))
        print("销卡成功！")
    else:
        print("该卡不存在！")


def account_modify():
    """
    更改卡片信息
    :return:
    """
    pass


def account_lock():
    """
    冻结账户
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    user_input = input("输入锁卡卡号：").strip()
    if user_input in data:
        data[user_input][0] == 0
        json.dump(data, open("%s/card.db" % settings.DB_DIR, 'w'))
        print("锁卡成功！")
    else:
        print("该卡不存在！")


def main():
    print(msg)
    while True:
        user_input = input("请选择：").strip()
        if user_input == '1':
            account_add()
        elif user_input == '2':
            account_del()
        elif user_input == '3':
            account_modify()
        elif user_input == '4':
            account_lock()
        else:
            print("选择无效！")
