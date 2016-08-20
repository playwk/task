#Author ZhengZhong,Jiang

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from conf import settings


"""
每天遍历个人信息文件，对每个账户的本期欠款做判断，只要大于0 就说明有欠款，
按欠款的万分之五计算利息，从可用余额中扣除当天产生的利息，只要用户
通过还款接口还清本期欠款，本期欠款就置0，之后不再产生利息。
"""

card_data = json.load(open("%s/card.db" % settings.DB_DIR), 'r')
for items in card_data.keys():
    if current_date[items][6] > 0:
        card_data[items][1] -= card_data[items][6] * 0.0005
json.dump(card_data, open('%s/card.db' % settings.DB_DIR, 'w'))