#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
MyFtp服务器端启动程序
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import server_argv_handler

if __name__ == "__main__":
    server_argv_handler.ArgvHandler(sys.argv)
