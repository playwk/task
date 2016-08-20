#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
MyFtp客户端核心模块，支持cd/dir/ls/mkdir/du/get/put/help等功能。
"""
import os
import sys
import json
import socket
import shutil
import hashlib
from conf import settings

class Client:
    """
    核心类。建立socket链接，调用功能方法。
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None
        self.user_name = None
        self.current_path = None
        # 在构造方法中调用链接方法和指令分发方法
        self.connect_server(self.host, self.port)
        self.cmd_call()

    def connect_server(self, host, port):
        """
        建立socket链接
        :param host: 主机ip
        :param port: 主机端口
        :return:
        """
        try:
            self.conn = socket.socket()
            self.conn.connect((host, port))
        except socket.error as e:
            print(e)
            exit("无法连接到服务器！")

    def cmd_call(self):
        """
        指令分发方法，通过字符串反射的方式调用不同的方法。
        :return:
        """
        # 在登陆服务器之前要求先进行用户登录验证
        self.current_path = self.login()
        # 此循环在用户使用客户端期间保持不变，提供永久服务。
        while True:
            # 设置提示符
            prompt = "[%s@%s %s] ftp> " % (self.user_name, self.host, self.current_path)
            cmd = input(prompt).strip()
            if not cmd:
                continue
            if cmd.startswith("login"):
                print("你已经登录了！")
                continue
            if cmd == "exit":
                self.conn.send("exit".encode())
                self.conn.close()
                exit("再见")
            cmd_list = cmd.split()
            # 设置指令格式
            instruction = "task_%s" % cmd_list[0]
            if hasattr(self, instruction):
                func = getattr(self, instruction)
                func(cmd_list)
            else:
                print("\033[31;0m无效的指令！\033[0m")
                Client.print_help_msg()
                continue

    def login(self):
        """
        用户登录。错误输入超过三次，退出程序。
        :return:
        """
        times = 0
        print("-----\033[31;0m欢迎使用MyFtp\033[0m-----")
        while True:
            if times >= 3:
                self.conn.send("exit".encode())
                self.conn.close()
                exit("输入错误超过3次，程序自动退出，再见！")
            user_name = input('请输入用户名：  ').strip()
            user_password = input('请输入密码：  ').strip()
            if not user_name:
                print('用户名不能为空！')
                continue
            if not user_password:
                print('密码不能为空！')
                continue
            hash_obj = hashlib.md5()
            hash_obj.update(user_password.encode())
            user_password = hash_obj.hexdigest()
            user = {"action": "login", "user_name": user_name, "password": user_password}
            json_str = json.dumps(user)
            self.conn.send(json_str.encode())
            res = self.conn.recv(1024)
            if res.decode() == "201":
                print(settings.RESPONSE_CODE["201"])
                times += 1
                continue
            else:
                print("200", settings.RESPONSE_CODE["200"])
                self.user_name = user_name
                pwd = os.sep
                # 返回当前操作系统的分隔符，作为用户家目录的代表
                return pwd

    def task_dir(self, cmd_list):
        """
        查看目录
        :param cmd_list: 命令参数
        :return:
        """
        if len(cmd_list) == 1:
            path = ""
        else:
            path = cmd_list[1]
        cmd_dict = {
                "action": "dir",
                "path": path
            }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        # 接收服务器发送过来的数据
        json_str = self.conn.recv(4096).decode()
        data = json.loads(json_str)
        # 对数据进行判断和分析
        if data == "401":
            print("401 %s" % settings.RESPONSE_CODE["401"])
        else:
            if not data:
                print("目录为空")
                return
            # 格式化打印目录结构
            print("\033[31;0m%s\033[0m 的目录" % self.current_path)
            for i in data:
                if i[0] == "d":
                    print("\033[34;0m%s\t\t\t\t\t\t<DIR>\033[0m" % i[1])
                else:
                    print("%s\t\t%.2fMB" % (i[1], i[2]/1024/1024))

    def task_ls(self, cmd_list):
        """
        ls命令实际是dir命令的复用
        :param cmd_list:
        :return:
        """
        self.task_dir(cmd_list)

    def task_cd(self, cmd_list):
        """
        切换路径
        :param cmd_list:
        :return:
        """
        # 生成命令字典
        if len(cmd_list) == 1:
            path = ""
        else:
            path = cmd_list[1]
        cmd_dict = {
            "action": "cd",
            "path": path
        }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        data = self.conn.recv(4096).decode()
        if data == "401":
            print("401 %s" % settings.RESPONSE_CODE["401"])
        else:
            # 如果服务器返回正常，将当前目录进行修改
            self.current_path = data

    def task_mkdir(self, cmd_list):
        """
        新建目录
        :param cmd_list:
        :return:
        """
        if len(cmd_list) == 1:
            print("未指定目录名！")
            return
        else:
            path = cmd_list[1]
        cmd_dict = {
            "action": "mkdir",
            "path": path
        }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        # 确认服务器发送的消息
        confirm = self.conn.recv(1024).decode()
        if confirm == "305":
            print("305 %s" % settings.RESPONSE_CODE["305"])
        else:
            print("308 %s" % settings.RESPONSE_CODE["308"])

    def task_du(self, cmd_list):
        """
        查询磁盘配额情况
        :param cmd_list:
        :return:
        """
        cmd_dict = {
            "action": "du"
        }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        data = self.conn.recv(4096)
        print(data.decode())

    def task_get(self, cmd_list):
        """
        下载文件
        :param cmd_list:
        :return:
        """
        # 处理源地址和目标地址
        if len(cmd_list) == 1:
            print("未指定要下载的文件！")
            return
        src_path = cmd_list[1]
        src_name = os.path.basename(src_path)
        if len(cmd_list) == 2:
            dst_path = os.path.join(settings.USER_HOME_DIR, self.user_name)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            dst_file = os.path.join(dst_path, src_name)
        elif len(cmd_list) == 3:
            if os.path.isdir(cmd_list[2]):
                dst_file = os.path.join(cmd_list[2], src_name)
            else:
                if not os.path.exists(os.path.dirname(cmd_list[2])):
                    print("目标路径不存在！")
                    return
                else:
                    dst_file = cmd_list[2]
        # 判断文件是否已存在
        if os.path.exists(dst_file):
            choice = input("目标文件已存在，覆盖yes，任意键取消！")
            if choice != "yes":
                print("取消下载任务！")
                return
        # 发送指令
        cmd_dict = {
        "action": "get",
        "file_path": src_path,
        }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        # 接收服务器确认信息
        confirm = self.conn.recv(1024).decode()
        if confirm == "404":
            print(settings.RESPONSE_CODE["404"])
            return
        # 获取文件信息
        file_info = json.loads(confirm)
        file_size = file_info["file_size"]
        # 生成临时文件
        temp_path = os.path.join(settings.USER_HOME_DIR, self.user_name, ".tmp")
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        temp_file = os.path.join(temp_path, file_info["md5"])
        # 判断是否有未完成的任务，可断点续传
        full_size = file_size
        temp_size = 0
        if os.path.exists(temp_file):
            print("发现未完成的下载任务，自动续传！")
            temp_size = os.stat(temp_file).st_size
            file_size -= temp_size
            msg = "402:%s" % temp_size
            self.conn.sendall(msg.encode())
        # 一切正常则开始接收文件
        self.conn.send("301".encode())
        rate = round(temp_size/full_size*100)
        with open(temp_file, "ab") as w:
            recv_size = 0
            while recv_size < file_size:
                data = self.conn.recv(4096)
                recv_size += len(data)
                w.write(data)
                # 打印任务进度条
                already = int((recv_size+temp_size)/full_size*100)
                if already == rate + 1:
                    self.view_bar(already)
                    rate += 1
        #生成MD5值
        hash_obj = hashlib.md5()
        with open(temp_file, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_obj.update(data)
        md5_str = hash_obj.hexdigest()
        print("\n\033[31;0mMD5校验码为\033[0m：%s" % md5_str)
        # 进行MD5值比较
        if md5_str == file_info["md5"]:
            shutil.copyfile(temp_file, dst_file)
            os.remove(temp_file)
            confirm = "306"
            print(settings.RESPONSE_CODE["306"])
            self.conn.sendall(confirm.encode())
        else:
            confirm = "307"
            print(settings.RESPONSE_CODE["307"])
            self.conn.sendall(confirm.encode())

    def task_put(self, cmd_list):
        """
        上传文件
        :param cmd_list:
        :return:
        """
        # 判断是否指定了要发送的文件
        if len(cmd_list) == 1:
            print("未指定上传文件！")
            return
        src_path = cmd_list[1]
        dst_path = ""
        if len(cmd_list) == 3:
            dst_path = cmd_list[2]
        # 判断文件是否存在
        if not os.path.isfile(src_path):
            print("文件不存在！")
            return
        # 获取文件的大小和MD5值
        file_name = os.path.basename(src_path)
        size = os.stat(src_path).st_size
        full_size = size
        hash_obj = hashlib.md5()
        with open(src_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_obj.update(data)
        md5_str = hash_obj.hexdigest()
        # 构建指令字典
        cmd_dict = {
            "action": "put",
            "file_name": file_name,
            "dst_path": dst_path,
            "size": size,
            "md5": md5_str
        }
        json_str = json.dumps(cmd_dict)
        self.conn.send(json_str.encode())
        # 接收服务器的确认信息，并进行判断
        confirm = self.conn.recv(1024).decode()
        if confirm == "400":
            print(settings.RESPONSE_CODE["400"])
            return
        if confirm == "401":
            print(settings.RESPONSE_CODE["401"])
            return
        transfered_data = 0
        rate = 0
        # 判断是否有未完成的任务
        if confirm.startswith("402"):
            print("发现未完成的任务，继续上次任务！")
            transfered_data = int(confirm.split(":")[1])
            size -= transfered_data
            rate = round(transfered_data/size*100)
            confirm = self.conn.recv(1024).decode()
        # 判断目标文件是否已经存在
        if confirm == "304":
            choice = input("目标文件已经存在，覆盖yes，任意键放弃！").strip()
            if choice != "yes":
                self.conn.sendall("abort".encode())
                return
            else:
                self.conn.sendall("continue".encode())
                confirm = self.conn.recv(1024).decode()
        print("\033[31;0mMD5校验码为\033[0m：%s" % md5_str)
        # 一切正常的话开始发送文件
        if confirm == "303":
            transfer_position = 0
            with open(src_path, "rb") as f:
                for line in f:
                    transfer_position += len(line)
                    if transfer_position > transfered_data:
                        self.conn.sendall(line)
                    already = int(transfer_position / full_size * 100)
                    if already == rate+1:
                        self.view_bar(already)
                        rate += 1
        # 接收任务确认信息
        confirm = self.conn.recv(1024).decode()
        if confirm == "306":
            print("")
            print(settings.RESPONSE_CODE["306"])
        else:
            print("")
            print(settings.RESPONSE_CODE["307"])

    def view_bar(self, already):
        """
        显示上传和下载任务的进度条
        :param already:
        :return:
        """
        number = int(already / 4)
        hashes = '#' * number
        spaces = ' ' * (25 - number)
        r = "\r\033[31;0m任务进度\033[0m：[%s%s]\033[32;0m%d%%\033[0m" % (hashes, spaces, already,)
        sys.stdout.write(r)
        sys.stdout.flush()

    def task_help(self, cmd_list):
        """
        打印帮助信息
        :param cmd_list:
        :return:
        """
        Client.print_help_msg()

    @staticmethod
    def print_help_msg():
        """
        提供帮助信息的静态方法
        :return:
        """
        msg = """
【帮助信息】：
    可执行命令：
    dir：     查看目录内容
    ls：      查看目录内容
    cd：      切换目录
    mkdir：   新建目录（因为平台的原因，暂不支持递归建立）
    du：      查看用户当前已用磁盘容量
    get：     下载文件
    put：     上传文件
    help:     查看帮助文件
    """
        print(msg)