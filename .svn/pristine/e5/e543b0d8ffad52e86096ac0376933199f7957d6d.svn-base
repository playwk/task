#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
客户端的运行参数处理模块。
"""
from modules import MyFtp_client_core


class ArgvHandler:
    """
    参数处理类，主要用来处理IP地址和port端口。
    """

    def __init__(self, args):
        self.args = args
        self.args_deal_with()

    def args_deal_with(self):
        """
        处理参数的方法
        :return:
        """
        if len(self.args) < 2:
            ArgvHandler.print_help_msg()
        else:
            host_port_list = self.args[1].split(":")
            host = host_port_list[0]
            port = int(host_port_list[1])
            client = MyFtp_client_core.Client(host, port)
            client.cmd_call()

    @staticmethod
    def print_help_msg():
        """
        打印运行帮助信息
        :return:
        """
        print("""请使用类似如下的命令运行FTP客户端：
python3 MyFtp_client.py 192.168.1.100:6666
""")
