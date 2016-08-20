#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5

"""
MyFtp服务器核心模块，实现了cd/dir/ls/mkdir/du/get/put/help等功能。
"""
import os
import json
import shutil
import hashlib
import socketserver
from conf import settings


class MyServer(socketserver.BaseRequestHandler):
    """
    继承了socketserver.BaseRequestHandler的类
    """
    def handle(self):
        """
        核心通信处理方法
        :return:
        """
        while True:
            try:
                # 接收客户端发来的信息，并加以分析
                cmd = self.request.recv(4096).decode()
                if cmd == "exit":
                    print("来自%s:%s的客户端主动断开连接..." % (self.client_address[0], self.client_address[1]))
                    break
                if not cmd:
                    print("客户端指令为空！")
                    break
                # 一切正常时，调用cmd_call方法
                self.cmd_call(cmd)
            except Exception as e:
                print(e)
                print("来自%s:%s的客户端主动断开连接..." % (self.client_address[0], self.client_address[1]))
                break

    def cmd_call(self, cmd_str):
        """
        指令分发机构，根据字符串反射相应的方法
        :param cmd_str: 命令参数
        :return:
        """
        # 对客户端发送过来的json数据进行解析
        cmd_dict = json.loads(cmd_str)
        # 获取命令动作
        command = cmd_dict["action"]
        if hasattr(self, command):
            func = getattr(self, command)
            # 调用对应的方法
            func(cmd_dict)
        else:
            print("错误的指令")

    def login(self, cmd_dict):
        """
        登录功能
        :param cmd_dict: 命令参数
        :return:
        """
        # 分析命令字典的数据
        name = cmd_dict["user_name"]
        password = cmd_dict["password"]
        if not os.path.exists(settings.USER_FILE):
            confirm = "201"
        else:
            if os.stat(settings.USER_FILE).st_size == 0:
                confirm = "201"
            else:
                with open(settings.USER_FILE) as f:
                    user_dict = json.load(f)
                if name not in user_dict:
                    confirm = "201"
                elif user_dict[name]["password"] != password:
                    confirm = "201"
                else:
                    # 当一切正常时，动态生成当前用户、用户磁盘配额、用户家目录三个字段
                    confirm = "200"
                    self.current_user = name
                    self.current_quota = user_dict[name]["quota"]
                    self.current_path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        self.request.sendall(confirm.encode())

    def dir(self, cmd_dict):
        """
        查看目录
        :param cmd_dict: 命令参数
        :return:
        """
        # 进行路径拼接和分析判断，限制客户端不能访问家目录以外的目录
        base_path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        if cmd_dict["path"].startswith("/"):
            path = os.path.join(base_path, cmd_dict["path"].lstrip("/"))
        else:
            path = os.path.join(self.current_path, cmd_dict["path"])
        path = os.path.abspath(path)
        if not path.startswith(base_path):
            self.request.sendall(json.dumps("401").encode())
            return
        if not os.path.exists(path):
            self.request.sendall(json.dumps("401").encode())
            return
        # 获得指定目录下的文件结构和文件大小，并以“d“和”f“的方式区分文件和目录
        dir_list = os.listdir(path)
        data_list = []
        for i in dir_list:
            file_path = os.path.join(path, i)
            list_1 = []
            if os.path.isdir(file_path):
                list_1.append("d")
                list_1.append(i)
                data_list.append(list_1)
            else:
                file_size = os.stat(file_path).st_size
                list_1.append("f")
                list_1.append(i)
                list_1.append(file_size)
                data_list.append(list_1)
        # 将生成的数据列表以json的格式发送给客户端
        json_str = json.dumps(data_list)
        self.request.sendall(json_str.encode())

    def cd(self, cmd_dict):
        """
        路径切换
        :param cmd_dict: 命令参数
        :return:
        """
        # 进行路径拼接和分析判断，限制客户端不能访问家目录以外的目录
        base_path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        if cmd_dict["path"].startswith("/"):
            path = os.path.join(base_path, cmd_dict["path"].lstrip("/"))
        else:
            path = os.path.join(self.current_path, cmd_dict["path"])
        path = os.path.abspath(path)
        if not os.path.exists(path):
            self.request.sendall("401".encode())
            return
        if not path.startswith(base_path):
            self.request.sendall("401".encode())
            return
        # 修改当前目录
        self.current_path = path
        # 截取相对路径字符串，并将其发送给客户端
        relative_path = path.replace(base_path, "")
        if not relative_path:
            relative_path = os.sep
        self.request.sendall(relative_path.encode())

    def mkdir(self, cmd_dict):
        """
        新建目录
        :param cmd_dict: 命令参数
        :return:
        """
        # 进行路径拼接和分析判断，限制客户端不能访问家目录以外的目录
        base_path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        if cmd_dict["path"].startswith("/"):
            dir_path = os.path.join(base_path, cmd_dict["path"].lstrip("/"))
        else:
            dir_path = os.path.join(self.current_path, cmd_dict["path"])
        if not dir_path.startswith(base_path):
            self.request.sendall("401".encode())
            return
        if os.path.exists(dir_path):
            self.request.sendall("305".encode())
            return
        else:
            os.mkdir(dir_path)
            self.request.sendall("308".encode())

    def du(self, cmd_dict):
        """
        查询磁盘配额使用情况
        :param cmd_dict:
        :return:
        """
        path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        # 递归遍历家目录下的所有目录和文件，计算文件大小的总和
        size = 0
        for root, dirs, files in os.walk(path):
            size += sum([os.stat(os.path.join(root, name)).st_size for name in files])
        free_size = (int(self.current_quota)*1024**3 - size)/1024**2
        mb_size = size / 1024 / 1024
        msg = "当前已用空间：%.2f MB\n当前可用空间：%.2f MB\n用户磁盘限额： %sGB"\
              % (mb_size, free_size, self.current_quota)
        self.request.sendall(msg.encode())

    def get(self, cmd_dict):
        """
        下载文件，支持断点续传
        :param cmd_dict: 命令参数
        :return:
        """
        # 分析指令字典的内容，判断路径和文件的正确与否，存在与否
        src_path = cmd_dict["file_path"]
        if src_path.startswith("/"):
            file_path = os.path.join(settings.USER_HOME_DIR, self.current_user, src_path.lstrip("/"))
        else:
            file_path = os.path.join(self.current_path, src_path)
        if not os.path.exists(file_path):
            self.request.sendall("404".encode())
            return
        # 获取文件大小和MD5码
        file_size = os.stat(file_path).st_size
        hash_obj = hashlib.md5()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_obj.update(data)
        md5_str = hash_obj.hexdigest()
        print(md5_str)
        # 生成消息字典，发送给客户端，并等待回应
        file_info = {
            "file_size": file_size,
            "md5": md5_str
        }
        json_str = json.dumps(file_info)
        self.request.sendall(json_str.encode())
        confirm = self.request.recv(1024).decode()
        # 判断是否有未完成的任务
        transfered_data = 0
        if confirm.startswith("402"):
            print("发现未完成的任务，继续上次任务！")
            transfered_data = int(confirm.split(":")[1])
            confirm = self.request.recv(1024).decode()
        # 如果一切正常，开始发送文件
        if confirm == "301":
            transfer_position = 0
            with open(file_path, "rb") as f:
                for line in f:
                    transfer_position += len(line)
                    if transfer_position > transfered_data:
                        self.request.sendall(line)
        # 确认文件发送成功
        confirm = self.request.recv(1024).decode()
        if confirm == "306":
            print(settings.RESPONSE_CODE["306"])
        else:
            print(settings.RESPONSE_CODE["307"])

    def put(self, cmd_dict):
        # 分析指令字典的内容
        file_name = cmd_dict["file_name"]
        file_size = cmd_dict["size"]
        dst_path = cmd_dict["dst_path"]
        # 判断磁盘限额是否足够
        base_path = os.path.join(settings.USER_HOME_DIR, self.current_user)
        used_size = 0
        for root, dirs, files in os.walk(base_path):
            used_size += sum([os.stat(os.path.join(root, name)).st_size for name in files])
        if file_size > (int(self.current_quota)*1024**3 - used_size):
            print("磁盘容量不足，拒绝上传！")
            self.request.sendall("400".encode())
            return
        # 设定临时文件
        temp_home = os.path.join(base_path, ".tmp")
        if not os.path.exists(temp_home):
            os.makedirs(temp_home)
        temp_file = os.path.join(temp_home, cmd_dict["md5"])
        # 判断是否有未完成的上传任务
        if os.path.exists(temp_file):
            print("发现未完成的上传任务")
            temp_size = os.stat(temp_file).st_size
            file_size -= temp_size
            msg = "402:%s" % temp_size
            self.request.sendall(msg.encode())
        # 分析文件路径
        if not dst_path:
            file_path = os.path.join(self.current_path, file_name)
        elif dst_path.startswith("/"):
            file_path = os.path.join(base_path, dst_path.lstrip("/"))
            if os.path.exists(os.path.dirname(file_path)):
                if not os.path.basename(file_path):
                    file_path = os.path.join(file_path, file_name)
            else:
                self.request.sendall("401".encode())
                return
        else:
            file_path = os.path.join(self.current_path, dst_path)
            if os.path.exists(os.path.dirname(file_path)):
                if not os.path.basename(file_path):
                    file_path = os.path.join(file_path, file_name)
            else:
                self.request.sendall("401".encode())
                return
        file_path = os.path.abspath(file_path)
        # 判断目标文件是否存在
        if os.path.exists(file_path):
            self.request.sendall("304".encode())
            confirm = self.request.recv(1024).decode()
            if confirm == "abort":
                print("客户端放弃传输文件")
                return
        # 如果一切正常，开始接收文件
        self.request.sendall("303".encode())
        with open(temp_file, "ab") as w:
            recv_size = 0
            while recv_size < file_size:
                data = self.request.recv(4096)
                w.write(data)
                recv_size += len(data)
        # 生成MD5值
        hash_obj = hashlib.md5()
        with open(temp_file, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_obj.update(data)
        md5_str = hash_obj.hexdigest()
        print(md5_str)
        # 进行MD5值对比
        if md5_str == cmd_dict["md5"]:
            shutil.copyfile(temp_file, file_path)
            os.remove(temp_file)
            confirm = "306"
            print(settings.RESPONSE_CODE["306"])
            self.request.sendall(confirm.encode())
        else:
            confirm = "307"
            print(settings.RESPONSE_CODE["307"])
            self.request.sendall(confirm.encode())
