#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Liu Jiang
# Python 3.5
"""
服务器配置文件
"""
import os

# 基本路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ftp账户信息存储目录
USER_FILE = os.path.join(BASE_DIR, "db", "user.json")
# 用户家目录
USER_HOME_DIR = os.path.join(BASE_DIR, "var", "users")
# ftp服务器地址及端口
IP_PORT = ("0.0.0.0", 6666)
# 响应状态码
RESPONSE_CODE = {
    "200": "登录成功",
    "201": "错误的用户名或者密码",
    "300": "服务器准备向客户端发送文件",
    "301": "客户端准备接受文件",
    "302": "客户端准备服务器向发送文件",
    "303": "服务器准备接受文件",
    "304": "目标文件已存在",
    "305": "目录已存在",
    "306": "文件传输成功，一致性校验通过!",
    "307": "文件传输失败!",
    "308": "目录建立成功!",
    "400": "磁盘容量不足，拒绝上传！",
    "401": "路径错误",
    "402": "存在未完成任务",
    "404": "源文件不存在",
}