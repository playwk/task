# Auther: ZhengZhong,Jiang

import os
import json
from conf import settings

def initialize_atm():
    """
    初始化ATM数据
    :return:
    """
    """
    for ATM
    """
    if os.path.exists('%s/user.db' % settings.DB_DIR) == False:
        data = {'admin': '123456'}
        json.dump(data, open('%s/user.db' % settings.DB_DIR, 'a'))
    if os.path.exists('%s/card.db' % settings.DB_DIR) == False:
        data = {"111":[15000, '123456', 15000, '22', '10']}
        json.dump(data, open('%s/card.db' % settings.DB_DIR, 'a'))
    if os.path.exists('%s/record.db' % settings.DB_DIR) == False:
        data = {}
        json.dump(data, open('%s/record.db' % settings.DB_DIR, 'a'))
    if os.path.exists('user.db') == False:
        print('初始化系统用户... ...')
        data = {'admin': ['123456', '1', '1', 0]}
        json.dump(data, open('user.db', 'a'))
        print('初始化系统用户完成！')
        print('Username: admin\nPassword: 123456')

def initialize_trade():
    """
    初始化购物商城数据
    :return:
    """
    if os.path.exists('%s/shopping_user.db' % settings.DB_DIR) == False:
        print('初始化系统用户... ...')
        data = {'admin': ['123456', '1', '1', '']}
        json.dump(data, open('%s/shopping_user.db' % settings.DB_DIR, 'a'))
        print('初始化系统用户完成！')
        print('Username: admin\nPassword: 123456')

    if os.path.exists('%s/shopping_history.db' % settings.DB_DIR) == False:
        print('初始化用户数据... ...')
        data = [['admin', '小米电视', 1, 3999, 'May-20-16 17:30:00']]
        json.dump(data,open('%s/shopping_history.db' % settings.DB_DIR, 'a'))
        print('初始化用户数据完成！')

    if os.path.exists('%s/shopping_car.db' % settings.DB_DIR) == False:
        data = [['admin', 'Mac', 1, 8999]]
        json.dump(data, open('%s/shopping_car.db' % settings.DB_DIR, 'a'))

    if os.path.exists('%s/shopping_product.db' % settings.DB_DIR) == False:
        data = {'家电': {'小米电视': [100,3999], 'Mac': [10,8999]},
                '手机': {'小米手机': [100,1999], 'iPhone': [10,5999]},
                '汽车': {'凯迪拉克': [5, 3000000], '玛莎拉蒂': [10, 3500000]}}
        json.dump(data, open('%s/shopping_product.db' % settings.DB_DIR, 'w'))