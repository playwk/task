# Auther: ZhengZhong,Jiang

import os
import pickle
from conf import settings

def init():
    """
    初始化数据
    :return:
    """
    if os.path.exists('%s/user.db' % settings.DB_DIR) == False:
        data = {'0': ['admin', '123', '2'], '1': ['st', '123', '0'], '2': ['te', '123', '1', '1000']}
        pickle.dump(data, open('%s/user.db' % settings.DB_DIR, 'wb'))
    if os.path.exists('%s/course.db' % settings.DB_DIR) == False:
        data = {"1":['撩妹必杀技', '100', 'alex', '第一式，幽默风趣；第二式，欲擒故纵']}
        pickle.dump(data, open('%s/course.db' % settings.DB_DIR, 'wb'))
    if os.path.exists('%s/student.db' % settings.DB_DIR) == False:
        data = {"1":['撩妹必杀技', '100', 'alex']}
        pickle.dump(data, open('%s/student.db' % settings.DB_DIR, 'wb'))