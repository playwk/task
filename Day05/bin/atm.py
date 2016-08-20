# Auther: ZhengZhong,Jiang
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import atm_index
from conf import settings


def main():
    atm_index.main()

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'start':
            main()
    except:
        print("请使用start参数启动程序")



