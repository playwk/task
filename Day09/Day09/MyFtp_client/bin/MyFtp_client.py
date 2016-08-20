#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
MyFtp客户端启动文件。
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import client_argv_handler

if __name__ == "__main__":
    client_argv_handler.ArgvHandler(sys.argv)
