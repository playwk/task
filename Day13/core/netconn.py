#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

import paramiko
import sys
import os
import socket
import getpass
import subprocess

from paramiko.py3compat import u
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import database

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        log = open('handle.log', 'a+', encoding='utf-8')
        flag = False
        temp_list = []
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            temp_list.append(x)
                        flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                import json

                if len(x) == 0:
                    break

                if x == '\t':
                    flag = True
                else:
                    temp_list.append(x)
                if x == '\r':
                    log.write(''.join(temp_list))
                    log.flush()
                    temp_list.clear()
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass


def run():
    run_who = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    who = run_who.stdout.read()
    result = database.session.query(database.BUsers).filter(database.BUsers.b_username == who).first()
    if result:
        gp_dict = {}
        for no,item in enumerate(result.user_group, 1):
            gp_dict[no] = item.group_name
    else:
        print("user not own any group !")
        exit()

    while True:
        for key in gp_dict.keys():
            print(key, gp_dict[key])
        choose = input(">>> ").strip()
        if choose.isdigit():
            choose_gp = gp_dict.get(int(choose))
            if not choose_gp:
                print("choose is invalid !")
                continue
        else:
            print("choose is invalid !")
            continue
        result_gp = database.session.query(database.Groups).filter(database.Groups.group_name ==
                choose_gp).first()
        if result_gp:
            ht_dict = {}
            for no,item in enumerate(result_gp.group_host, 1):
                ht_dict[no] = item.host_ip
            break
        else:
            print("no host in hostgroup !")
            continue

    while True:
        for key in ht_dict.keys():
            print(key, ht_dict[key])
        choose = input(">>> ").strip()
        if choose.isdigit():
            choose_ht = ht_dict.get(int(choose))
            if not choose_ht:
                print("choose is invalid !")
                continue
        else:
            print("choose is invalid !")
            continue
        result_ht = database.session.query(database.Hosts).filter(database.Hosts.host_ip ==
                choose_ht).first()
        host_port = database.session.query(database.Hosts.host_port).filter(database.Hosts.host_ip ==
                choose_ht).first()
        host_port = host_port[0]
        if result_ht:
            ur_dict = {}
            for no,item in enumerate(result_ht.host_user, 1):
                ur_dict[no] = item.username
            break
        else:
            print("no user viable !")
            continue

    while True:
        for key in ur_dict.keys():
            print(key, ur_dict[key])
        choose = input(">>> ").strip()
        if choose.isdigit():
            choose_ur = ur_dict.get(int(choose))
            if not choose_ur:
                print("choose is invalid !")
                continue
        else:
            print("choose is invalid !")
            continue
        password = database.session.query(database.Users.password).filter(database.Users.username ==
                choose_ur).first()
        password = password[0]
        usercert = database.session.query(database.Users.usercert).filter(database.Users.username ==
                choose_ur).first()
        usercert = usercert[0]
        certpass = database.session.query(database.Users.certpass).filter(database.Users.username ==
                choose_ur).first()
        certpass = certpass[0]
        break


    tran = paramiko.Transport(choose_ht, host_port,)
    tran.start_client()

    default_auth = "p"
    auth = input('Auth by (p)assword or (r)sa key[%s] ' % default_auth)
    if len(auth) == 0:
        auth = default_auth
    if auth == 'r':
        default_path = usercert
        try:
            key = paramiko.RSAKey.from_private_key_file(usercert)
        except paramiko.PasswordRequiredException:
            key = paramiko.RSAKey.from_private_key_file(usercert, certpass)
        tran.auth_publickey(choose_ur, key)
    else:
        tran.auth_password(choose_ur, password)

    # 打开一个通道
    chan = tran.open_session()
    # 获取一个终端
    chan.get_pty()
    # 激活器
    chan.invoke_shell()

    interactive_shell(chan)

    chan.close()
    tran.close()


if __name__ == '__main__':
    run()
