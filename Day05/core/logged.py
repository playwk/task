# Auther: ZhengZhong,Jiang

from conf import settings
import logging


def log(user, info, ):
    """
    日志功能
    :param arg:
    :param info:
    :return:
    """
    logg = logging.getLogger('ftp_logger')
    logg.setLevel(logging.INFO)
    fh = logging.FileHandler('%s/record.log' % settings.LOG_DIR, encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(user)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logg.addHandler(fh)
    logg.info(info)
    logg.removeHandler(fh)
