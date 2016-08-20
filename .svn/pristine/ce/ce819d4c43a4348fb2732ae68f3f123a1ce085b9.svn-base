#Author ZhengZhong,Jiang

import os,json,prettytable
from functools import wraps

status = 0
current_user = ''

if os.path.exists('user.db') == False:
    print('初始化系统用户... ...')
    data = {'admin':['123456', '超级用户', 'admin@gmail.com', 10000]}
    json.dump(data,open('user.db', 'a'))
    print('初始化系统用户完成！')
    print('Username: admin\nPassword: 123456')

msg = """
+-----------------------------+
          1.系统登录
          2.账号注册
          3.修改密码
          4.修改权限
          5.个人信息
          6.管理用户
+-----------------------------+
( 按q/Q 退出程序 )
"""

def outer1(func):
    """
    使用wraps装饰，保留原函数调用，通过__wrapped__属性解除装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(args):
        """
        用于装饰用户为登录状态才可以执行的函数
        :param func:
        :return:
        """
        if status == 0:
            print("\033[31;1m请先登录系统!\033[0m")
        else:
            func(args)
    return wrapper


def outer2(func):
    """
    用于装饰用户为登录状态并且是管理员才可以执行的函数
    :param func:
    :return:
    """
    def inner():
        if status == 0:
            print("\033[31;1m请先登录系统!\033[0m")
        else:
            if status == 3:
                func()
            else:
                print("\033[31;1m权限不足！\033[0m")
    return inner


def login():
    """
    用户登录
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    input_user = input("请输入用户名：").strip()
    if user_info.get(input_user) == None:
        print('\033[31,1m用户名不存在！\033[0m')
    else:
        input_pass = input("请输入密码：")
        if user_info.get(input_user)[0] != input_pass:
            print("密码错误！")
        else:
            global status
            #status初始值为0，表示用户未登录，程序运行到此处标记用户状态为已登录
            status = 1
            global current_user
            current_user = input_user
            if user_info.get(input_user)[1] == '普通用户':
                #程序运行到此处表示当前登录用户是普通用户身份
                status = 2
                print("\033[32;1m当前登录用户：{0},用户类型：普通用户\033[0m".format(current_user))
            else:
                # 程序运行到此处表示当前登录用户是超级用户身份
                status = 3
                print("\033[32;1m当前登录用户：{0},用户类型：超级用户\033[0m".format(current_user))


def regist():
    """
    用户注册
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    flag = True
    while flag:
        input_user = input("用户名：").strip()
        if user_info.get(input_user) != None:
            print("\033[31;1m该用户名已注册！\033[0m")
        else:
            input_pass = input("密码：")
            try:
                print('\033[31;1m注意：普通用户请输入0，超级用户请输入1\033[0m')
                input_type = int(input("注册用户类型：").strip())
                if input_type != 1 and input_type != 0:
                    print("\033[31;1m请输入数字0或1！\033[0m")
                    continue
                else:
                    flag = False
            except:
                print("\033[31;1m输入不合法！\033[0m")
        input_email = input("邮箱地址：").strip()
        while True:
            input_mobile = input("手机号码：").strip()
            if not input_mobile.isdigit():
                print("\033[31;1m手机号码无效！\033[0m")
            else:
                break
    if input_type == 0:
        user_info[input_user] = [input_pass, '普通用户', input_email, input_mobile, ]
    elif input_type == 1:
        user_info[input_user] = [input_pass, '超级用户', input_email, input_mobile, ]
    json.dump(user_info,open('user.db', 'w'))
    print("\033[32;1m注册成功！\033[0m")


@outer1
def modify_pwd(args):
    """
    修改用户密码
    :param args:
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    while True:
        input_oldpwd = input("旧密码：")
        if input_oldpwd == user_info.get(args)[0]:
            input_newpwd = input("新密码：")
            input_re_newpwd = input("再次输入新密码：")
            if input_newpwd == input_re_newpwd:
                user_info.get(args)[0] = input_newpwd
                json.dump(user_info,open('user.db','w'))
                print("\033[32;1m密码修改成功！\033[0m")
                break
            else:
                print("\033[31;1m两次密码输入不一致！\033[0m")
        else:
            print("\033[31;1m旧密码不正确！\033[0m")


@outer2
def modify_role():
    """
    只有超级用户才有权限操作
    修改用户权限
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    while True:
        username = input("要修改权限的用户名: ").strip()
        if user_info.get(username) != None:
            user_role = user_info[username][1]
        else:
            print("\033[31;1m要修改权限的用户不存在！\033[0m")
            continue
        print('\033[31;1m注意：普通用户请输入0，超级用户请输入1\033[0m')
        input_type = int(input("请输入用户类型：").strip())
        if input_type != 1 and input_type != 0:
            print("\033[31;1m请输入数字0或1！\033[0m")
        else:
            break
    if input_type == 0:
        user_info[username][1] = '普通用户'
    elif input_type == 1:
        user_info[username][1] = '超级用户'
    json.dump(user_info,open('user.db', 'w'))
    print("\033[32;1m权限修改成功！\033[0m")


@outer1
def print_info(*args,**kwargs):
    """
    使用prettytables对用户信息类表格打印
    :param args:
    :param kwargs:
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    filed = ['账户名称', '帐户密码', '账户类型', '邮箱地址', '联系电话', ]
    print_out = prettytable.PrettyTable(filed)
    print_out.align['账户名称'] = '1'
    print_out.padding_width = 1
    for info in args:
        print_out.add_row([info, user_info[info][0],
                           user_info[info][1],
                           user_info[info][2],
                           user_info[info][3]])
    print(print_out)


@outer2
def usermgt():
    """
    只有超级用户才有权限操作
    主要实现超级用户对系统账户的增删查
    :return:
    """
    user_info = json.load(open('user.db', 'r'))
    print_info.__wrapped__(*list(json.load(open('user.db', 'r')).keys()))
    while True:
        mgt = ['增加用户', '删除用户', '查询信息', ]
        for action in enumerate(mgt):
            print('.'.join([str(action[0] + 1), mgt[action[0]]]))
        print('(按其他任意键返回上级菜单)')
        choose = input("请选择：").strip()
        if choose == '1':
            add_record = input("使用 \"|\" 分隔，依次输入账户名称、帐户密码、账户类型、邮箱地址、联系电话：\n")
            if add_record.split('|')[2] != '0' and add_record.split('|')[2] != '1':
                print("\033[31;1m用户类型不合法！（必须0或者1）\033[0m")
                continue
            else:
                if add_record.split('|')[2].strip() == '0':
                    user_type = '普通用户'
                elif add_record.split('|')[2].strip() == '1':
                    user_type = '超级用户'
            if not add_record.split('|')[4].isdigit():
                print("\033[31;1m联系电话无效！\033[0m")
            user_info[add_record.split('|')[0].strip()] = [add_record.split('|')[1],
                                                    user_type,
                                                    add_record.split('|')[3].strip(),
                                                    add_record.split('|')[4].strip(), ]
            json.dump(user_info,open('user.db','w'))
            print_info.__wrapped__(*list(json.load(open('user.db', 'r')).keys()))
        elif choose == '2':
            del_record = input("输入要删除的用户：").strip()
            if user_info.get(del_record) != None:
                del user_info[del_record]
                json.dump(user_info, open('user.db', 'w'))
                print_info.__wrapped__(*list(json.load(open('user.db', 'r')).keys()))
            else:
                print('\033[32;1m该用户不存在！\033[0m')
        elif choose == '3':
            query_record = input("输入要查询的关键字：")
            result_dict = []
            for items in user_info:
                record = "{0}{1}{2}{3}{4}".format(items,user_info[items][0],
                                                  user_info[items][1],
                                                  user_info[items][2],
                                                  user_info[items][3], )
                if query_record in record:
                    result_dict.append(items)
            print_info.__wrapped__(*result_dict)
        else:
            break


while True:
    print(msg)
    choose = input("请选择：").strip()
    if choose == '1':
        login()
    elif choose == '2':
        regist()
    elif choose == '3':
        modify_pwd(current_user)
    elif choose == '4':
        modify_role()
    elif choose == '5':
        print_info(current_user)
    elif choose == '6':
        usermgt()
    elif choose == 'q' or choose == 'Q':
        exit()
    else:
        print("\033[31;1m选择无效！\033[0m")