# Auther: ZhengZhong,Jiang

import os
import json
from conf import settings
from core import shopping_admin
from core import shopping_user
from core import initialize

msg = '''

        1.登录
        2.注册

按任意键退出。。。
'''


def main():
    initialize.initialize_trade()
    while True:
        print("购物商城系统".center(22, '-'))
        print(msg)
        choose = input('请输入选择：')
        if choose == '2':
            try:
                while True:
                    user_add = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
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
            user_card = input('请输入绑定支付卡号：').strip()
            while True:
                if user_card not in json.load(open("%s/card.db" % settings.DB_DIR, 'r')):
                    user_card = 0
                    print("绑定卡号无效! ")
                else:
                    break
            data = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
            data[user_name] = [user_pass, user_type, '1', user_card]
            json.dump(data, open('%s/shopping_user.db' % settings.DB_DIR, 'w'))
        elif choose == '1':
            lock_temp = []
            user_info = json.load(open('%s/shopping_user.db' % settings.DB_DIR, 'r'))
            user_temp = list(user_info.keys())
            while True:
                username = input('用户名：')
                password = input('密码：')
                user_msg = username in user_temp
                if user_msg:
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
                                shopping_admin.admin(username)
                            else:
                                #调用普通用户登录成功后的方法
                                shopping_user.user(username)
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
                    user_info[username][2] = '1'
                    json.dump(user_info, open('%s/shopping_user.db' % settings.DB_DIR, 'w'))
                    exit()
                continue
            continue
