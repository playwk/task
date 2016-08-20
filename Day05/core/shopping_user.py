# Author ZhengZhong,Jiang

import json
import prettytable
import datetime
from conf import settings
from core.atm_user import pay


msg_user = '''
-------------------------
        1.开始购物
        2.已购清单
        3.一键下单
        4.历史订单
        5.修改卡号
        6.个人信息
-------------------------
按菜单号选择操作，按b返回，按q退出。。。
'''


def conn_card(cardno):
    atm_info = json.load(open('%s/card.db' % settings.DB_DIR, 'r'))
    if cardno not in atm_info.keys():
        print("无效的卡号！")
        return "invalid"
    else:
        passwd = atm_info[cardno][2]
        money = atm_info[cardno][1]
        return "%s|%s" % (money, passwd)

def user(username):
    userdata = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
    cardno = userdata[username][3]
    money = json.load(open('%s/card.db' % settings.DB_DIR, 'r'))[cardno][1]
    while True:
        print(msg_user)
        choose = input('请输入选择：')
        if choose == 'b':
            continue
        elif choose == 'q':
            exit()
        elif choose == '1':
            items_temp = []
            product_info = json.load(open('%s/shopping_product.db' % settings.DB_DIR, 'r'))
            while True:
                print('-------------------------')
                for items in enumerate(list(product_info.keys()),start=1):
                    print(('%d.%s'.center(25) % (items[0],items[1])))
                    items_temp.append([items[0],items[1]])
                print('-------------------------')
                print('按菜单号选择操作，按b返回，按q退出。。。')
                choose_type = input('请输入选择：')
                try:
                    choose_type = int(choose_type)
                except:
                    if choose_type == 'b':
                        break
                    elif choose_type == 'q':
                        exit()
                    else:
                        print('您的选择不合法，请重新输入！')
                        continue
                #把商品类别编号和商品类别按字典存放
                element = {}
                for items in items_temp:
                    element[items[0]] = items[1]
                if element.get(int(choose_type)) == None:
                    print('您的选择不合法，请重新输入！')
                    continue
                else:
                    product_temp = []
                    product_dict = product_info[element[int(choose_type)]]
                    filed = ['商品编号','商品名称','剩余数量','商品价格']
                    print_out = prettytable.PrettyTable(filed)
                    print_out.align['商品编号'] = '1'
                    print_out.padding_width = 1
                    product_element = {}
                    #打印商品信息
                    for product in enumerate(product_dict, start=1):
                        product_temp.append([product[0], product[1]])
                        # 把商品编号和商品名称按字典存放
                        for items in product_temp:
                            product_element[items[0]] = items[1]
                        print_out.add_row([product[0], product_element[product[0]],
                                           product_dict[product_element[product[0]]][0],
                                           product_dict[product_element[product[0]]][1]])
                    print(print_out)
                    print('账户余额:[%d]' % float(money))
                    while True:
                        print('按菜单号选择操作，按b返回，按q退出。。。')
                        choose_product = input('请输入选择：')
                        if choose_product == 'b':
                            break
                        elif choose_product == 'q':
                            exit()
                        else:
                            try:
                                if product_element.get(int(choose_product)) != None:
                                    product_num = int(input('请输入购买数量：'))
                                    if product_num > product_dict[product_element.get(int(choose_product))][0]:
                                        print('存货不足！请减少购买数量或更改购买商品！')
                                        continue
                                    else:
                                        product_add = [username,product_element.get(int(choose_product)),product_num,
                                                       product_num * product_dict[product_element.\
                                                           get(int(choose_product))][1]]
                                        data = json.load(open('%s/shopping_car.db' % settings.DB_DIR,'r'))
                                        new_data = data
                                        times = 0
                                        for items in enumerate(data):
                                            if items[1][0] == product_add[0] and items[1][1] == product_add[1]:
                                                num_new = items[1][2] + product_add[2]
                                                money_new = items[1][3] + product_add[3]
                                                items_new = [items[1][0],items[1][1],num_new,money_new]
                                                new_data.pop(items[0])
                                                new_data.append(items_new)
                                            else:
                                                times += 1
                                                if times == len(data):
                                                    new_data.append(product_add)
                                                    break
                                        json.dump(new_data,open('%s/shopping_car.db' % settings.DB_DIR, 'w'))
                                        print('已成功添加至已购清单，可继续选购其他商品！')
                                else:
                                    print('选择的，请重新输入！')
                            except:
                                print('您的选择不合法，请重新输入！')
        elif choose == '2':
            # while True:
            pay_total = 0
            filed = ['商品名称', '购买数量', '购买价格']
            print_out = prettytable.PrettyTable(filed)
            print_out.align['商品名称'] = '1'
            print_out.padding_width = 1
            for pay_info in json.load(open('%s/shopping_car.db' % settings.DB_DIR, 'r')):
                if pay_info[0] == username:
                    print_out.add_row([pay_info[1], pay_info[2], pay_info[3]])
                    pay_total += pay_info[3]
            print_out.add_row(['', '总额', pay_total])
            print('账户余额:[%d]' % float(money))
            print(print_out)
        elif choose == '3':
            pay_total = 0
            pay_record = []
            # while True:
                # pay_total = 0
                # 计算选择的商品数量×商品价格是否大于账户余额，如果大于则提示，否则扣款！
                # pay_record = []

            for pay_info in json.load(open('%s/shopping_car.db' % settings.DB_DIR, 'r')):
                if pay_info[0] == username:
                    pay_record.append([username, pay_info[1], pay_info[2], pay_info[3],
                                       datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')])
                    pay_total += pay_info[3]  #  消费金额
            res = conn_card(cardno)
            money = float(res.split('|')[0])
            if res != "invalid":
                shopping_info = json.load(open('%s/shopping_car.db' % settings.DB_DIR, 'r'))
                pay_status = pay(cardno, pay_total, "网购")
                if pay_status == 1:
                    print('当前消费:[%d],账户余额不足,请充值！' % pay_total)
                elif pay_status == 2:
                    print("账户冻结！")
                else:
                    pay_record = json.load(open('%s/shopping_history.db' % settings.DB_DIR, 'r'))
                    shopping_car = json.load(open('%s/shopping_car.db' % settings.DB_DIR, 'r'))
                    for pay_money in shopping_car:
                        if pay_money[0] == username:
                            pay_record.append([username, pay_money[1], pay_money[2], pay_money[3],
                                               datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')])
                    json.dump(pay_record, open('%s/shopping_history.db' % settings.DB_DIR, 'w'))
                    # 付完款清空用户当前的购物车
                    new_data = []
                    for items in enumerate(shopping_info):
                        if items[1][0] != username:
                            new_data.append(items[1])
                    json.dump(new_data, open('%s/shopping_car.db' % settings.DB_DIR, 'w'))
                    print('当前消费:[%d],账户余额:[%d]' % (pay_total, pay_status))
        elif choose == '4':
            filed = ['商品名称', '购买数量', '购买价格','购买时间']
            print_out = prettytable.PrettyTable(filed)
            print_out.align['商品名称'] = '1'
            print_out.padding_width = 1
            data = json.load(open('%s/shopping_history.db' % settings.DB_DIR,'r'))
            for items in data:
                if items[0] == username:
                    print_out.add_row([items[1], items[2], items[3],items[4]])
            print(print_out)
        elif choose == '5':
            user_info = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
            while True:
                cardno = input('请输入要绑定关联的有效卡号：')
                res = conn_card(cardno)
                if res != 'invalid':
                    passwd = input("请输入该卡的支付密码：")
                    if passwd == res.split('|')[1]:
                        user_info[username][3] = cardno
                        json.dump(user_info, open('%s/shopping_user.db' % settings.DB_DIR, 'w'))
                        print('绑定成功！')
                        break
                    else:
                        print('密码错误！')

        elif choose == '6':
            user_info = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
            filed = ['账号名称', '账号密码', '账号角色', '账号状态', '绑定卡号']
            print_out = prettytable.PrettyTable(filed)
            print_out.align['账号编号'] = '1'
            print_out.padding_width = 1
            print_out.add_row([username, user_info[username][0], user_info[username][1],
                               user_info[username][2], user_info[username][3]])
            print(print_out)