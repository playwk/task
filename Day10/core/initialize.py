# Auther: ZhengZhong,Jiang

import os
import json
import sys
import hashlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import settings


def initialize():
    """
    初始化数据
    :return:
    """
    if os.path.exists('%s/user.db' % settings.DB_DIR) == False:
        password = '123456'
        password_auth = hashlib.md5(password.encode('utf-8'))
        pwd = password_auth.hexdigest()
        print(pwd)
        print('初始化系统用户... ...')
        data = {'admin': [pwd, 200]}
        json.dump(data, open('%s/user.db' % settings.DB_DIR, 'w'))
        print('初始化系统用户完成！')
        print('Username: admin\nPassword: 123456')

