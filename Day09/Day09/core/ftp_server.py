"""Author ZhengZhong,Jiang"""

import os
import sys
import socketserver
import subprocess
import json
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import settings


class Comm(socketserver.BaseRequestHandler):
    user = ''
    user_state = 0
    current_path = user
    whoami = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE).stdout.read().decode()

    def comm_cd(self, *args, **kwargs):
        file_path = args[0].get('file_path')
        if file_path == '..':
            if Comm.current_path == Comm.user:
                subprocess.Popen('cd %s/%s' % (settings.DATA_DIR, Comm.user),
                                 shell=True)
                self.request.send(bytes('200', encoding='utf8'))
                Comm.current_path = Comm.user
            else:
                file_path = "%s" % Comm.current_path
                path_list = file_path.split('/')
                path_list.pop()
                file_path = ''.join(path_list)
                cmd = subprocess.Popen('cd %s' % file_path,
                                       shell=True, stderr=subprocess.PIPE)
                res = cmd.stderr.read()
                send_data = bytes('200', encoding="utf8")
                self.request.send(send_data)
                Comm.current_path = file_path
        else:
            cmd = subprocess.Popen('cd %s%s/%s' % (settings.DATA_DIR, Comm.current_path, file_path),
                                   shell=True, stderr=subprocess.PIPE)
            res = cmd.stderr.read()
            if len(res):
                send_data = bytes('404', encoding="utf8")
                self.request.send(send_data)
                send_data = bytes("目录不存在！", encoding='utf8')
                self.request.send(send_data)
            else:
                send_data = bytes('200', encoding="utf8")
                self.request.send(send_data)
                Comm.current_path = '%s/%s' % (Comm.current_path, file_path)
                Comm.current_path = Comm.current_path

    def comm_mkdir(self, *args, **kwargs):
        user_name = args[0].get('username')
        file_path = args[0].get('file_path')
        subprocess.Popen('mkdir -p %s%s/%s' % (settings.DATA_DIR, Comm.current_path, file_path), shell=True)

    def comm_ls(self, *args, **kwargs):
        print('####################################')
        print(Comm.current_path)
        print('####################################')
        file_path = args[0].get('file_path')
        if file_path == '.':
            file_path = ''
        cmd = subprocess.Popen('ls -l %s%s/%s' % (settings.DATA_DIR, Comm.current_path, file_path),
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = cmd.stdout.read()
        re_code = bytes('200', encoding='utf8')
        self.request.send(re_code)
        if len(res):
            res = re.sub(Comm.whoami.strip(), Comm.user, res.decode())
            # print(res)
            res = bytes(res, encoding='utf8')
            self.request.send(res)
        else:
            res = cmd.stderr.read()
            self.request.send(res)

    def comm_put(self, *args, **kwargs):
        data = json.load(open('%s/user.db' % settings.DB_DIR, 'r'))
        quota = data.get(Comm.user)[2]
        # user_name = args[0].get('username')
        file_name = args[0].get('file_name')
        file_size = args[0].get('file_size')
        cmd = subprocess.Popen('du -sb %s%s' % (settings.DATA_DIR, Comm.user),
                               shell=True, stdout=subprocess.PIPE)
        use_size = cmd.stdout.read().split()[0].strip()
        if file_size + int(use_size) >= quota*1024*1024:
            self.request.send(bytes("磁盘空间不够！", encoding='utf8'))
        else:
            # server_response = {"status": 200}
            self.request.send(bytes("200", encoding='utf-8'))
            f = open('%s/%s/%s' % (settings.DATA_DIR, Comm.current_path, file_name), 'wb')
            recv_size = 0
            while recv_size < file_size:
                data = self.request.recv(4096)
                f.write(data)
                recv_size += len(data)
                print('file_size: %s  recvsize:%s' % (file_size, recv_size))
            print("file recv success")
            f.close()

    def comm_get(self, *args, **kwargs):
        user_name = args[0].get('username')
        file_name = args[0].get('file_name')
        file_size = os.stat('%s%s/%s' % (settings.DATA_DIR, user_name, file_name)).st_size
        file_info = {'file_size': file_size}
        self.request.send(bytes(json.dumps(file_info), encoding='utf8'))
        client_confirmation_msg = self.request.recv(1024)
        confirm_data = json.loads(client_confirmation_msg.decode())
        f = open('%s%s/%s' % (settings.DATA_DIR, user_name, file_name), 'rb')
        send_size = 0
        if confirm_data['status'] == 200:
            for line in f:
                self.request.send(line)
            print("file send done")
        f.close()


class Ftp(Comm):

    def reg(self):
        database = json.load(open("%s/user.db" % settings.DB_DIR, 'r'))
        recv_data = self.request.recv(1024)
        recv_dict = json.loads(recv_data.decode(), encoding='utf8')
        user_list = list(database.keys())
        if recv_dict['username'] in user_list:
            self.request.send(bytes('该用户已存在！', encoding='utf8'))
        else:
            subprocess.Popen('mkdir %s/%s' % (settings.DATA_DIR, recv_dict['username']), shell=True)
            database[recv_dict['username']] = [recv_dict['password'], "/home/%s" % recv_dict['username'], 500]
            json.dump(database, open("%s/user.db" % settings.DB_DIR, 'w'))
            self.request.send(bytes('注册成功！', encoding='utf8'))

    def auth(self):
        while True:
            database = json.load(open("%s/user.db" % settings.DB_DIR, 'r'))
            data = self.request.recv(1024)
            recv_dict = json.loads(data.decode(), encoding='utf8')
            user_list = list(database.keys())
            if recv_dict['username'] in user_list:
                if recv_dict['password'] == database[recv_dict['username']][0]:
                    self.request.send(bytes("登录成功，欢迎！", encoding='utf8'))
                    Comm.user = recv_dict['username']
                    print(recv_dict)
                    Comm.user = Comm.user.strip()
                    Comm.user_state = 1
                    Comm.current_path = '%s' % Comm.user
                    state_code = json.dumps({'user_state': 1})
                    self.request.send(bytes(state_code, encoding='utf8'))
                    break
                else:
                    self.request.send(bytes("密码错误！", encoding='utf8'))
                    state_code = json.dumps({'user_state': 0})
                    self.request.send(bytes(state_code, encoding='utf8'))
                    break
            else:
                self.request.send(bytes("用户不存在！", encoding='utf8'))
                state_code = json.dumps({'user_state': 0})
                self.request.send(bytes(state_code, encoding='utf8'))
                break

    def handle(self):
        while True:
            choose = self.request.recv(1024)
            choose = choose.decode()
            if choose == 'reg':
                self.reg()
            else:
                self.auth()
                if Comm.user_state == 1:
                    while True:
                        data = self.request.recv(1024)
                        print(data.decode())
                        if len(data) == 0:
                            continue
                        else:
                            print('[%s] says: %s' % (self.client_address, data.decode()))
                            task_data = json.loads(data.decode())
                            task_data['username'] = self.user
                            task_action = task_data.get("action")
                            if hasattr(self, "comm_%s" % task_action):
                                func = getattr(self, "comm_%s" % task_action)
                                print(func)
                                print(task_data)
                                func(task_data)
                            else:
                                print("task action is not supported", task_action)

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 8000), Ftp)
    server.serve_forever()
