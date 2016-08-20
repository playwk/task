#Author ZhengZhong,Jiang

import socket
import json
import os
import sys
import time
import re
import getpass
import hashlib

ip_port = ('127.0.0.1', 8000)

c = socket.socket()

c.connect(ip_port)

msg = """
1.登录
2.注册
"""


class Action:
    send_data = ''

    @staticmethod
    def auth():
        """
        客户端认证
        :return:
        """
        c.send(bytes('login', encoding='utf8'))
        username = input("用户名：").strip()
        password = getpass.getpass("密码: ")
        password_auth = hashlib.md5(password.encode('utf-8'))
        pwd = password_auth.hexdigest()

        data = {'username': username, 'password': pwd}
        data = json.dumps(data)
        c.send(bytes(data, encoding='utf8'))

        auth_msg = c.recv(4096)
        print(auth_msg.decode())

        data = c.recv(4096)
        data = data.decode()
        data = json.loads(data)
        user_state = data.get("user_state")

        return data

    @staticmethod
    def reg():
        """
        客户端注册
        :return:
        """
        c.send(bytes('reg', encoding='utf8'))
        username = input("用户名：").strip()
        password = input("密码：")
        password_auth = hashlib.md5(password.encode('utf-8'))
        pwd = password_auth.hexdigest()

        data = {'username': username, 'password': pwd}
        data = json.dumps(data)

        c.send(bytes(data, encoding='utf8'))

        re_msg = c.recv(1024)

        print(re_msg.decode())

    @staticmethod
    def calehash(args):
        """
        文件hash摘要
        :param args:
        :return:
        """
        m = hashlib.md5()
        with open(args, 'rb')as fp:
            while True:
                blk = fp.read(4096)
                if not blk:break
                m.update(blk)
        return m.hexdigest()

    @staticmethod
    def comm_put(file_path):
        """
        put 命令方法
        :param file_path:
        :return:
        """
        if os.path.isfile(file_path):
            file_size = os.stat(file_path).st_size
            print('file_size:',file_size, type(file_size))
            # 对windows和linux路径分隔符不一致做统一处理
            file_name = re.split(r'[\\/]', file_path).pop()
            file_hash = Action.calehash(file_path)
            print('file:%s size:%s' % (file_path, file_size))
            msg_data = {"action": "put",
                        "file_name": file_name,
                        "file_size": file_size,
                        "file_hash": file_hash}
            c.send(bytes(json.dumps(msg_data), encoding="utf8"))
            confirm_data = c.recv(1024).decode()
            if confirm_data == '200':
                print("start sending file ", file_name)
                f = open(file_path, 'rb')
                send_size = 0
                rate = 0
                old_rate = 0
                for line in f:
                    c.send(line)
                    # 根据已传输的大小比例计算进度条 '#' 的个数
                    send_size += len(line)
                    rate = send_size * 50 // file_size
                    # 如果进度条的长度比上次有增加则刷新进度条
                    if rate - old_rate > 0:
                        r = '\r[%s%s]%d%%' % (rate * '#', (50 - rate) * ' ', rate * 2)
                        sys.stdout.write(r)
                        sys.stdout.flush()
                    old_rate = rate
                recv_data = c.recv(1024).decode()
                print('\n%s' % '文件上传完成！')
                print(recv_data)
            else:
                print(confirm_data)
        else:
            print("\033[31;1mfile [%s] is not exist\033[0m" % file_path)

    @staticmethod
    def comm_get(file_path):
        """
        get 命令方法
        :param file_path:
        :return:
        """
        Action.send_data = {'action': 'get', 'file_name': file_path}
        Action.send_data = json.dumps(Action.send_data)
        c.send(bytes(Action.send_data, encoding='utf8'))
        data = c.recv(1024)
        if data.decode() == '200':
            if os.path.exists(file_path):
                file_size = os.stat(file_path).st_size
                file_status = '401'
                file_info = json.dumps({'file_size': file_size, 'file_status': file_status})
                c.sendall(bytes(file_info, encoding='utf8'))
                client_response = {"status": 200}
                c.send(bytes(json.dumps(client_response), encoding='utf8'))
                f = open(file_path, 'ab')
                recv_size = file_size
                old_rate = recv_size * 50 // int(file_size)
                while recv_size < int(file_size):
                    data = c.recv(4096)
                    f.write(data)
                    recv_size += len(data)
                    rate = recv_size * 50 // int(file_size)
                    if rate - old_rate > 0:
                        r = '\r[%s%s]%d%%' % (rate * '#', (50 - rate) * ' ', rate * 2)
                        sys.stdout.write(r)
                        sys.stdout.flush()
                    old_rate = rate
                f.close()
                print('\n%s' % '文件下载完成！')
                file_hash = c.recv(1024).decode()
                file_comp = Action.calehash(file_path)
                if file_hash == file_comp:
                    print('文件校验一致!')
                else:
                    print('文件校验不一致！请重传！')
            else:
                c.sendall(bytes('200', encoding='utf8'))
                file_size = json.loads(c.recv(1024).decode()).get('file_size')
                client_response = {"status": 200}
                c.send(bytes(json.dumps(client_response), encoding='utf8'))
                print('file:%s size:%s' % (file_path, file_size))
                f = open(file_path, 'wb')
                recv_size = 0
                old_rate = 0
                while recv_size < int(file_size):
                    data = c.recv(4096)
                    f.write(data)
                    recv_size += len(data)
                    rate = recv_size * 50 // int(file_size)
                    if rate - old_rate > 0:
                        r = '\r[%s%s]%d%%' % (rate * '#', (50 - rate) * ' ', rate * 2)
                        sys.stdout.write(r)
                        sys.stdout.flush()
                    old_rate = rate
                f.close()
                print('\n%s' % '文件下载完成！')
                file_hash = c.recv(1024).decode()
                file_comp = Action.calehash(file_path)
                if file_hash == file_comp:
                    print('文件校验一致!')
                else:
                    print('文件校验不一致！请重传！')
        else:
            print('文件不存在！')

    @staticmethod
    def comm_mkdir(file_path):
        """
        mkdir 创建目录方法
        :param file_path:
        :return:
        """
        # 对路径中特殊的'\'处理
        file_path = re.split(r'\\', r'%s' % file_path)
        # 拼接文件路径名称
        file_path = ''.join(file_path)
        Action.send_data = {'action': 'mkdir', 'file_path': file_path}
        c.send(bytes(json.dumps(Action.send_data), encoding='utf8'))

    @staticmethod
    def comm_cd(file_path):
        """
        cd 切换目录方法
        :param file_path:
        :return:
        """
        # 对路径中特殊的'\'处理
        file_path = re.split(r'\\', r'%s' % file_path)
        # 拼接文件路径名称
        file_path = ''.join(file_path)
        Action.send_data = {'action': 'cd', 'file_path': file_path}
        c.send(bytes(json.dumps(Action.send_data), encoding='utf8'))
        recv_data = c.recv(1024).decode()
        if recv_data == '404':
            recv_data = c.recv(1024)
            print(recv_data.decode())

    @staticmethod
    def comm_ls(file_path='.'):
        """
        ls 查看路径下的文件及文件夹信息
        :param file_path:
        :return:
        """
        # 对路径中特殊的'\'处理
        file_path = re.split(r'\\', r'%s' % file_path)
        # 拼接文件路径名称
        file_path = ''.join(file_path)
        Action.send_data = {'action': 'ls', 'file_path': file_path}
        c.send(bytes(json.dumps(Action.send_data), encoding='utf8'))
        recv_data = c.recv(1024).decode()
        if recv_data == '200':
            recv_data = c.recv(1024).decode()
            print(recv_data)

    @staticmethod
    def comm_exit():
        """
        退出程序
        :return:
        """
        exit()


while True:
    print(msg)
    choose = input(">>> ").strip()
    if choose == '1':
        res_auth = Action.auth()
        while res_auth:
            send_data = input(">>> ").strip()
            if len(send_data) == 0:continue
            cmd_list = send_data.split()

            if len(cmd_list) == 1:
                task_type = cmd_list[0]
                if task_type == 'exit':
                    Action.comm_exit()
                if task_type == 'ls':
                    Action.comm_ls()
                else:
                    print('无效的指令！')
                    continue
            elif len(cmd_list) == 2:
                task_type = cmd_list[0]
                if task_type == 'put':
                    Action.comm_put(cmd_list[1])
                elif task_type == 'get':
                    Action.comm_get(cmd_list[1])
                elif task_type == 'mkdir':
                    Action.comm_mkdir(cmd_list[1])
                elif task_type == 'cd':
                    Action.comm_cd(cmd_list[1])
                elif task_type == 'ls':
                    Action.comm_ls(cmd_list[1])
            else:
                print('无效的指令！')
                continue
        continue
    elif choose == '2':
        Action.reg()
        continue
    else:
        exit()


