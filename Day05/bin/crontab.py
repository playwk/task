#Author ZhengZhong,Jiang
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from conf import settings


"""
每月10号运行该脚本，对所有用户的负债情况计算，计算完的值存入用户信息中的本期欠款，
方便每天的计划任务来计算和统计生成的利息，用户还款的情况只会变更用户可用金额的变化，
不会更改本期欠款，除非可用余额大于等于信用额度（即用户还清欠款没有负债情况），则会
将本期欠款置0，一旦置0，则不再产生利息。
"""


card_data = json.load(open("%s/card.db" % settings.DB_DIR), 'r')
for items in card_data.keys():
    if card_data[items][3] - card_data[items][1] > 0:
        card_data[items][6] = card_data[items][3] - card_data[items][1]
json.dump(card_data, open('%s/card.db' % settings.DB_DIR, 'w'))