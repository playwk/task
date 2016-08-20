#Author ZhengZhong,Jiang

import os,json,prettytable,datetime


if os.path.exists('user.db') == False:
    print('初始化系统用户... ...')
    data = {'admin':['123456','1','1',0]}
    json.dump(data,open('user.db', 'a'))
    print('初始化系统用户完成！')
    print('Username: admin\nPassword: 123456')


if os.path.exists('history.db') == False:
    print('初始化用户数据... ...')
    data = [['admin','小米电视',1,3999,'May-20-16 17:30:00']]
    json.dump(data,open('history.db', 'a'))
    print('初始化用户数据完成！')

if os.path.exists('shop_car.db') == False:
    data = [['admin','Mac',1,8999]]
    json.dump(data,open('shop_car.db', 'a'))

if os.path.exists('product.db') == False:
    data = {'家电':{'小米电视':[100,3999],'Mac':[10,8999]},
            '手机':{'小米手机':[100,1999],'iPhone':[10,5999]},
            '汽车':{'凯迪拉克': [5, 3000000], '玛莎拉蒂': [10, 3500000]}}
# json.dump(data,open('product.db', 'a')) if os.path.exists('product.db') == False


msg = '''
-------------------------
        1.登录
        2.注册
        3.退出
-------------------------
按菜单号选择操作，按b返回，按q退出。。。
'''


msg_user = '''
-------------------------
        1.开始购物
        2.已购清单
        3.一键下单
		4.历史订单
		5.账户充值
-------------------------
按菜单号选择操作，按b返回，按q退出。。。
'''


msg_admin = '''
-------------------------
        1.用户管理
        2.商品管理
		3.账户余额
-------------------------
按菜单号选择操作，按b返回，按q退出。。。
'''


def user(username):
    '''

    :param username:
    :return:
    '''
    while True:
        print(msg_user)
        choose = input('请输入选择：')
        if choose == 'b':
            continue
        elif choose == 'q':
            exit()
        elif choose == '1':
            items_temp = []
            product_info = json.load(open('product.db','r'))
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
                    for product in enumerate(product_dict,start=1):
                        product_temp.append([product[0],product[1]])
                        # 把商品编号和商品名称按字典存放
                        for items in product_temp:
                            product_element[items[0]] = items[1]
                        print_out.add_row([product[0],product_element[product[0]],\
                                           product_dict[product_element[product[0]]][0], \
                                           product_dict[product_element[product[0]]][1]])
                    print(print_out)
                    money = json.load(open('user.db', 'r'))[username][3]
                    print('账户余额:[%d]' % money)
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
                                    if product_num > product_dict[product[1]][0]:
                                        print('存货不足！请减少购买数量或更改购买商品！')
                                        continue
                                    else:
                                        product_add = [username,product_element.get(int(choose_product)),product_num,\
                                                       product_num * product_dict[product_element.\
                                                           get(int(choose_product))][1]]
                                        data = json.load(open('shop_car.db','r'))
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
                                        json.dump(new_data,open('shop_car.db','w'))
                                        print('已成功添加至已购清单，可继续选购其他商品！')
                                else:
                                    print('选择的，请重新输入！')
                            except:
                                print('您的选择不合法，请重新输入！')
        elif choose == '2':
            while True:
                pay_total = 0
                filed = ['商品名称', '购买数量', '购买价格']
                print_out = prettytable.PrettyTable(filed)
                print_out.align['商品名称'] = '1'
                print_out.padding_width = 1
                for pay in json.load(open('shop_car.db', 'r')):
                    if pay[0] == username:
                        print_out.add_row([pay[1], pay[2], pay[3]])
                        pay_total += pay[3]
                print_out.add_row(['', '总额', pay_total])
                money = json.load(open('user.db', 'r'))[username][3]
                print('账户余额:[%d]' % money)
                print(print_out)
                print('按b返回，按q退出。。。')
                choose = input('请输入选择：')
                if choose == 'b':
                    break
                elif choose == 'q':
                    exit()
                else:
                    print('您的选择不合法，请重新输入！')
        elif choose == '3':
            pay_total = 0
            pay_record = []
            while True:
                # pay_total = 0
                # 计算选择的商品数量×商品价格是否大于账户余额，如果大于则提示，否则扣款！
                # pay_record = []
                data = json.load(open('history.db', 'r'))
                for pay in json.load(open('shop_car.db', 'r')):
                    if pay[0] == username:
                        pay_record.append([username, pay[1], pay[2], pay[3], \
                                           datetime.datetime.now().strftime('%b-%d-%y %H:%M:%S')])
                        pay_total += pay[3]  # 消费金额
                money = json.load(open('user.db', 'r'))[username][3]  # 账户余额
                if pay_total > money:
                    print('当前消费:[%d],账户余额:[%d],请充值！' % (pay_total, money))
                else:
                    data = json.load(open('history.db', 'r'))
                    temp = data
                    data.extend(pay_record)
                    json.dump(temp, open('history.db', 'w'))
                    data = json.load(open('user.db', 'r'))
                    #减掉当前用户余额
                    data[username][3] -= pay_total
                    #加上admin用户余额
                    data['admin'][3] += pay_total
                    json.dump(data, open('user.db', 'w'))
                    print('当前消费:[%d],账户余额:[%d]' % (pay_total, data[username][3]))
                    # 付完款清空用户当前的购物车
                    data = json.load(open('shop_car.db', 'r'))
                    new_data = []
                    for items in enumerate(data):
                        if items[1][0] != username:
                            new_data.append(items[1])
                    json.dump(new_data, open('shop_car.db', 'w'))
                print('按b返回，按q退出。。。')
                choose = input('请输入选择：')
                if choose == 'b':
                    break
                elif choose == 'q':
                    exit()
                else:
                    print('您的选择不合法，请重新输入！')
        elif choose == '4':
            while True:
                filed = ['商品名称', '购买数量', '购买价格','购买时间']
                print_out = prettytable.PrettyTable(filed)
                print_out.align['商品名称'] = '1'
                print_out.padding_width = 1
                data = json.load(open('history.db','r'))
                for items in data:
                    if items[0] == username:
                        print_out.add_row([items[1], items[2], items[3],items[4]])
                print(print_out)
                print('按b返回，按q退出。。。')
                choose = input('请输入选择：')
                if choose == 'b':
                    break
                elif choose == 'q':
                    exit()
                else:
                    print('您的选择不合法，请重新输入！')
        elif choose == '5':
            while True:
                try:
                    money = json.load(open('user.db', 'r'))[username][3]
                    print('账户余额:[%d]' % money)
                    print('输入充值金额，按b返回，按q退出。。。')
                    choose = input('请输入选择：')
                    data = json.load(open('user.db', 'r'))
                    data[username][3] = int(choose) + money
                    json.dump(data, open('user.db', 'w'))
                    money = json.load(open('user.db', 'r'))[username][3]
                except:
                    if choose == 'b':
                        break
                    elif choose == 'q':
                        exit()
                    else:
                        print('您的选择不合法，请重新输入！')


def admin(username):
    '''

    :param username:
    :return:
    '''
    while True:
        print(msg_admin)
        choose = input('请输入选择：')
        if choose == 'b':
            continue
        elif choose == 'q':
            exit()
        elif choose == '1':
            items_temp = []
            user_info = json.load(open('user.db','r'))
            while True:
                for items in enumerate(list(user_info.keys())):
                    items_temp.append([items[0],items[1]])
                filed = ['账号编号', '账号名称', '账号密码', '账号角色', '账号状态', '账号余额']
                print_out = prettytable.PrettyTable(filed)
                print_out.align['账号编号'] = '1'
                print_out.padding_width = 1
                for user in items_temp:
                    print_out.add_row([user[0],user[1],user_info[user[1]][0],user_info[user[1]][1], \
                                       user_info[user[1]][2],user_info[user[1]][3]])
                print(print_out)
                print('按菜单号选择操作，按b返回，按q退出。。。')
                user_temp = []
                choose = input('请输入选择：')
                try:
                    choose = int(choose)
                    for userdata in items_temp:
                        user_temp.append(userdata[0])
                    if user_temp.count(choose) == 0:
                        print('选择的用户无效！请重新选择！')
                        continue
                    else:
                        print('已选择为用户[%s]修改信息！' % items_temp[int(choose)])
                        choose_pass = input('请输入账号密码：')
                        choose_role = input('请输入账号角色：')
                        choose_stat = input('请输入账号状态：')
                        user_data = [items_temp[choose][1],[choose_pass,choose_role, \
                                     choose_stat,user_info[items_temp[choose][1]][3]]]
                        print(user_data)
                        user_info = json.load(open('user.db', 'r'))
                        del user_info[items_temp[choose]]
                        user_info[items_temp[choose]] = user_data
                        json.dump(user_info,open('user.db','w'))
                        print(json.load(open('user.db', 'r')))
                except:
                    if choose == 'b':
                        break
                    elif choose == 'q':
                        exit()
                    else:
                        print('您的选择不合法，请重新输入！')
        elif choose == '2':
            product_info = json.load(open('product.db', 'r'))


while True:
    print(msg)
    choose = input('请输入选择：')
    if choose == '2':
        try:
            while True:
                user_add = json.load(open('user.db','r'))
                user_list = list(user_add.keys())
                user_name = input('请输入注册用户名：')
                if user_list.count(user_name) >0:
                    print('该用户名已被占用,请使用其他用户名注册！')
                    continue
                else:
                    break
        except IOError as err:
            print('File error: %s' % str(err))
            exit()
        user_pass = input('请输入注册密码：')
        print('\033[31;1m注意：如果是管理员用户，请输入1，其他输入都将默认为普通用户\033[0m')
        role = input('是否管理员：')
        if role == '1':
            user_type = '1'
        else:
            user_type = '0'
        data = json.load(open('user.db','r'))
        data[user_name] = [user_pass, user_type, '1', 0]
        json.dump(data,open('user.db','w'))
    elif choose == '1':
        count = 0
        lock_temp = []
        user_temp = {}
        user_info = json.load(open('user.db', 'r'))
        user_temp = list(user_info.keys())
        while True:
            username = input('用户名：')
            password = input('密码：')
            user_msg = username in user_temp
            if user_msg == True:
                if user_info[username][2] == '0':
                    print('用户已被锁定！请联系管理员解锁！返回上级菜单按b,继续按c，其他任意键退出！')
                    choose = input('请输入选择：')
                    if choose == 'b':
                        break
                    elif choose == 'c':
                        continue
                    else:
                        exit()
                else:
                    if password == user_info[username][0]:
                        if user_info[username][1] == '1':
                            #调用管理员登录成功后的方法
                            admin(username)
                        else:
                            #调用普通用户登录成功后的方法
                            shop_car = {}
                            user(username)
                    else:
                        print('密码错误！')
                        lock_temp.append(username)
            else:
                    print('该用户不存在！返回上级菜单按b,继续按c，其他任意键退出！')
                    choose = input('请输入选择：')
                    if choose == 'b':
                        break
                    elif choose == 'c':
                        continue
                    else:
                        exit()
            if lock_temp.count(username) >2:
                print('密码重试次数太多，用户被锁定！')
                userupdate = json.load(open('user.db','r'))
                user_info[username][2] = '1'
                json.dump(user_info,open('user.db','w'))
                exit()
            continue
        continue