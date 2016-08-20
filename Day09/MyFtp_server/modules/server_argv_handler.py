#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
服务器端启动参数处理模块。可分别启动主服务器
和服务器后台管理程序。
"""

import socketserver
from conf import settings
from modules import MyFtp_server_core
from modules import manage_core


class ArgvHandler:

    def __init__(self, args):
        self.args = args
        self.args_deal_with()

    def args_deal_with(self):
        """
        参数处理方法。
        :return:
        """
        if len(self.args) < 2:
            ArgvHandler.print_help_msg()
        else:
            action = self.args[1]
            if hasattr(self, action):
                func = getattr(self, action)
                func()
            else:
                ArgvHandler.print_help_msg()

    def start(self):
        """
        启动服务器
        :return:
        """
        server = socketserver.ThreadingTCPServer(settings.IP_PORT, MyFtp_server_core.MyServer)
        server.serve_forever()

    def manage(self):
        """
        启动服务器后台管理程序
        :return:
        """
        manage_core.main()

    @staticmethod
    def print_help_msg():
        print("""请使用如下的运行方式：
python3 MyFtp_server.py start      启动FTP服务器
python3 MyFtp_server.py manage     启动FTP后台管理程序
""")
