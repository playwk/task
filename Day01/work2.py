#Author ZhengZhong,Jiang

msg='''
---------------------------
1.登录
2.注册
3.退出
---------------------------
按1选择登录，按2选择注册，按其他任意键选择退出
'''
flag = True
lock_dict = {}
while flag:
    print(msg)
    std_in = input('请输入您的选择: ')
    #用户注册
    if std_in == '2':
        username = input('请输入用户名: ')
        password = input('请输入密码: ')
        info = open('user.info','r')
        #判断用户是否重复注册，只接受新用户注册并写入user.info文件
        user_statu = 1
        for each_user in info.readlines():
            each_user = each_user.strip('\n').split()
            each_user_name = each_user[0]
            if username == each_user_name:
                print('该用户名已被注册!')
                break
            else:
                user_statu = 1
        info.close()
        if user_statu == 0:
            continue
        info = open('user.info','a')
        info.write("%s %s\n" % (username,password))
        info.close()
        print('注册成功！')
    #用户登录
    elif std_in == '1':
        username = input('请输入用户名: ')
        password = input('请输入密码: ')
        if username not in lock_dict.keys():
            lock_dict[username] = 0
        lock = open('user.lock','r')
        lock_statu = 1
        #判断用户是否锁定，若锁定则无法登陆
        for lock_user in lock.readlines():
            lock_user = lock_user.strip('\n')
            if username == lock_user:
                print('该用户已被锁定，无法登录！')
                break
            else:
                lock_statu = 1
        lock.close()
        if lock_statu == 0:
            continue
        #判断用户是否密码输错超过三次，超过则写入user.lock文件，标记锁定
        if lock_dict[username] < 2:
            info = open('user.info', 'r')
            last_line  = info.readlines()[-1]
            info.close()
            info = open('user.info', 'r')
            for user_info in info.readlines():
                result = user_info.split()
                result_username = result[0]
                result_password = result[1]
                if result_username == username and result_password == password:
                    print('登录成功！')
                    flag = False
                    break
                elif result_username == username and result_password != password:
                    print('用户名或密码不正确！')
                    lock_dict[username] += 1
                    break
                else:
                    if user_info == last_line:
                        print('用户不存在！')
            info.close()
        else:
            lock = open('user.lock', 'a')
            lock.write("%s\n" % username)
            lock.close()
            print('尝试次数过多，用户被锁定!')
            flag = False
            break
    #退出循环，结束
    else:
        flag = False
