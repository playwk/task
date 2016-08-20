#Author ZhengZhong,Jiang

import socket
import json

ip_port = ('12.12.11.135', 8000)

c = socket.socket()

c.connect(ip_port)

username = input("用户名：").strip()
password = input("密码: ").strip()

data = {'username': username, 'password': password}
data = json.dumps(data)

c.send(bytes(data, encoding='utf-8'))

