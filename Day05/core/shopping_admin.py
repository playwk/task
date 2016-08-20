# Auther: ZhengZhong,Jiang

import os
import json
import prettytable
from conf import settings


msg_admin = '''
-------------------------
        1.个人信息
        2.用户管理
-------------------------
按菜单号选择操作，按b返回，按q退出。。。
'''


def admin(username):
    while True:
        print(msg_admin)
        choose = input('请输入选择：')
        if choose == 'b':
            continue
        elif choose == 'q':
            exit()
        elif choose == '1':
            items_temp = []
            user_info = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
            # for items in enumerate(list(user_info.keys())):
            #     items_temp.append([items[0], items[1]])
            filed = ['账号名称', '账号密码', '账号角色', '账号状态', '绑定卡号']
            print_out = prettytable.PrettyTable(filed)
            print_out.align['账号编号'] = '1'
            print_out.padding_width = 1
            print_out.add_row([username, user_info[username][0], user_info[username][1],
                               user_info[username][2], user_info[username][3]])
            print(print_out)
            print('按菜单号选择操作，按b返回，按q退出。。。')
        elif choose == '2':
            for items in enumerate(list(user_info.keys())):
                items_temp.append([items[0], items[1]])
            filed = ['账号编号', '账号名称', '账号密码', '账号角色', '账号状态', '绑定卡号']
            print_out = prettytable.PrettyTable(filed)
            print_out.align['账号编号'] = '1'
            print_out.padding_width = 1
            for user in items_temp:
                print_out.add_row([user[0], user[1], user_info[user[1]][0], user_info[user[1]][1],
                                   user_info[user[1]][2], user_info[user[1]][3]])
            print(print_out)
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
                    user_data = [items_temp[choose][1], [choose_pass, choose_role,
                                                         choose_stat, user_info[items_temp[choose][1]][3]]]
                    print(user_data)
                    user_info = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
                    del user_info[items_temp[choose]]
                    user_info[items_temp[choose]] = user_data
                    json.dump(user_info, open('%s/shopping_user.db' % settings.DB_DIR, 'w'))
                    print(json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r')))
            except:
                if choose == 'b':
                    break
                elif choose == 'q':
                    exit()
                else:
                    print('您的选择不合法，请重新输入！')
        else:
            print('您的选择不合法，请重新输入！')