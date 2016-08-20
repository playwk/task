# Auther: ZhengZhong,Jiang

import time
import datetime
import json
from prettytable import PrettyTable
from conf import settings
from core.logged import log

msg = """

-----ATM+ 信用卡管理系统-----

1.个人信息
2.取现
3.转账
4.还款
5.账单
"""


def userinfo(cardno):
    """
    查看用户信息
    :param cardno:
    :return:
    """
    user_info = json.load(open('%s/card.db' % settings.DB_DIR, 'r'))
    filed = ['卡号', '卡片状态', '可用金额', '卡片密码', '信用额度', '账单日期', '还款日期', '本期欠款']
    print_out = PrettyTable(filed)
    print_out.align['账户名称'] = '1'
    print_out.padding_width = 1
    user_info[cardno][0] = '激活' if user_info[cardno][0] == 1 else '冻结'
    print_out.add_row([cardno, user_info[cardno][0],
                       user_info[cardno][1],
                       user_info[cardno][2],
                       user_info[cardno][3],
                       user_info[cardno][4],
                       user_info[cardno][5],
                       user_info[cardno][6],
                       ])
    print(print_out)
    log(cardno, "查看个人信息")


def pay(cardno, money, type="取现"):
    """
    支付接口
    :param cardno:
    :param money:
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    if data[cardno][0] == 1:
        if data[cardno][1] > money:
            if type == "取现":
                data[cardno][1] = data[cardno][1] - money * 1.05
            else:
                data[cardno][1] -= money
            json.dump(data, open("%s/card.db" % settings.DB_DIR, 'w'))
            record = json.load(open("%s/record.db" % settings.DB_DIR, 'r'))
            user_record = {'type': type, 'money': -money,
                           'balance': data[cardno][1],
                           'date_time': datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')}
            if cardno in record:
                record[cardno].append(user_record)
            else:
                record[cardno] = []
                record[cardno].append(user_record)
            json.dump(record, open("%s/record.db" % settings.DB_DIR, 'w'))
            # "操作成功！
            return data[cardno][1]
        else:
            # "余额不足！
            return 1
    else:
        # "账户冻结！
        return 2


def cost(cardno):
    """
    取现接口
    :param cardno:
    :param type:
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    money = input("输入金额：").strip()
    if money.isdigit():
        money = int(money)
        pay(cardno, money)
    else:
        print("金额必须是数字！")


def repay(cardno, money, type="还款"):
    """
    还款接口
    :param cardno:
    :param money:
    :return:
    """
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    if data[cardno][0] == 1:
        data[cardno][1] += money
        if data[cardno][1] >= 15000:
            data[cardno][6] = 0
        json.dump(data, open("%s/card.db" % settings.DB_DIR, 'w'))
        record = json.load(open("%s/record.db" % settings.DB_DIR, 'r'))
        user_record = {'type': type, 'money': +money,
                       'balance': data[cardno][1],
                       'date_time': datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')}
        if cardno in record:
            record[cardno].append(user_record)
        else:
            record[cardno] = []
            record[cardno].append(user_record)
        json.dump(record, open("%s/record.db" % settings.DB_DIR, 'w'))
        return 1
    else:
        print("账户冻结！")
        return 2


def forward(cardno):
    """
    转账接口
    :param cardno:
    :return:
    """
    accept_cardno = input("输入转账卡号：").strip()
    data = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    if accept_cardno in data:
        money = input("输入金额：").strip()
        if money.isdigit():
            money = int(money)
            pay(cardno, money, type="转出")
            repay(accept_cardno, money, type="转入")
            log(cardno, "向 %s 转账 %d 成功！" % (accept_cardno, money))
        else:
            print("金额必须是数字！")
    else:
        log(cardno, "转账失败，%s 账户不存在！" % accept_cardno)
        print("卡号不存在！")


def bill(cardno):
    """
    账单生成
    :param cardno:
    :return:
    """
    print("""
    1.已出账单
    2.未出账单
    """)
    current_date = datetime.datetime.today().day
    current_year = datetime.datetime.today().year
    current_month = datetime.datetime.today().month
    if current_month == 1:
        last_month = 12
        current_year -= 1
    else:
        last_month = current_month - 1
    current_date = datetime.datetime.today().day
    current_time= datetime.datetime.strptime(datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S'),'%b-%d-%y %H:%M:%S')
    data = json.load(open("%s/record.db" % settings.DB_DIR, 'r'))
    userdata = json.load(open("%s/card.db" % settings.DB_DIR, 'r'))
    repay_date = userdata[cardno][4]
    last_month = current_month - 1
    bill_list = []
    user_input = input("请选择：")
    if user_input == '1':
        if current_time > current_time.replace(current_year, current_month, repay_date):
            if current_month == 1:
                bill_starttime = current_time.replace(current_year, last_month, repay_date)
                bill_endtime = current_time.replace(current_year + 1, current_month, repay_date)
            else:
                bill_starttime = current_time.replace(current_year, last_month, repay_date)
                bill_endtime = current_time.replace(current_year, current_month, repay_date)
        else:
            bill_starttime = current_time.replace(current_year, current_month - 2, repay_date)
            bill_endtime = current_time.replace(current_year, current_month - 1, repay_date)
        for items in data[cardno]:
            convert_time = datetime.datetime.strptime(items['date_time'], "%b-%d-%y %H:%M:%S")
            if bill_starttime < convert_time < bill_endtime:
                bill_list.append(items)
        filed = ['操作类别', '操作金额', '账户余额', '操作日期']
        print_out = PrettyTable(filed)
        print_out.align['操作类别'] = '1'
        print_out.padding_width = 1
        for info in bill_list:
            print_out.add_row([info['type'],
                               info['money'],
                               info['balance'],
                               info['date_time']])
        print(print_out)
        if len(bill_list) == 0:
            debt = userdata[cardno][3]
        else:
            debt = userdata[cardno][3] - bill_list.pop()['balance']
        if debt > 0:
            if len(bill_list) == 0:
                print("本期应还金额：%d" % (userdata[cardno][3]))
            else:
                print("本期应还金额：%d" % (userdata[cardno][3] - bill_list.pop()['balance']))
        else:
            print("本期应还金额：0")

        print("总负债：%d" % (userdata[cardno][3]-userdata[cardno][1]))
        log(cardno, "打印已出账单！")
    elif user_input == '2':
        if current_time > current_time.replace(current_year, current_month, repay_date):
            bill_starttime = current_time.replace(current_year, current_month, repay_date)
        else:
            bill_starttime = current_time.replace(current_year, last_month, repay_date)
        for items in data[cardno]:
            convert_time = datetime.datetime.strptime(items['date_time'], "%b-%d-%y %H:%M:%S")
            if bill_starttime < convert_time:
                bill_list.append(items)
        filed = ['操作类别', '操作金额', '账户余额', '操作日期']
        print_out = PrettyTable(filed)
        print_out.align['操作类别'] = '1'
        print_out.padding_width = 1
        for info in bill_list:
            print_out.add_row([info['type'],
                               info['money'],
                               info['balance'],
                               info['date_time']])
        print(print_out)
        debt = userdata[cardno][3] - bill_list.pop()['balance']
        if debt > 0:
            print("本期应还金额：%d" % (userdata[cardno][3] - bill_list.pop()['balance']))
        else:
            print("本期应还金额：0")
        print("总负债：%d" % (userdata[cardno][3] - userdata[cardno][1]))
        log(cardno, "打印未出账单！")


def main(cardno):
    while True:
        print(msg)
        user_input = input("请输入：").strip()
        if user_input == '1':
            userinfo(cardno)
        elif user_input == '2':
            res = cost(cardno)
            if res == 1:
                log(cardno, "取现 余额不足! ")
            elif res == 2:
                log(cardno, "取现 账户冻结！")
            else:
                log(cardno, "取款成功! ")
        elif user_input == '3':
            forward(cardno)
        elif user_input == '4':
            money = input("输入金额：").strip()
            if money.isdigit():
                money = int(money)
                res = repay(cardno, money)
                if res == 1:
                    log(cardno, "还款 %d 成功！" % money)
                else:
                    log(cardno, "还款 %d 失败，账户冻结！" % money)
            else:
                print("金额必须是数字！")
        elif user_input == '5':
            bill(cardno)
        elif user_input == 'q':
            exit()
        else:
            print("选择无效！")


