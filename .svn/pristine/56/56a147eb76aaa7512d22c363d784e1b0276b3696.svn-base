# Auther: ZhengZhong,Jiang

import re

msg = """
============================
        1.获取ha记录
        2.增加ha记录
        3.删除ha记录
============================
退出请按q...
"""

def query_info(args,file='ha_proxy.conf'):
    """
    定义一个函数用来查询backend对应节点下是否存在相关的配置记录
    """
    with open('ha_proxy.conf','r') as f:
        result = set()
        data = {}
        temp = []
        flag = 0
        for each_line in f:
            if re.match('backend', each_line) != None:
                flag += 1
            if flag == 1:
                if re.match('backend', each_line) != None:
                    data[each_line.strip().split()[1]] = temp
                elif each_line.strip() != '':
                    temp_dict = {}
                    temp_list = (each_line.strip().split())
                    temp_dict[temp_list[0]] = '%s %s' % (temp_list[1],temp_list[1])
                    temp_dict[temp_list[3]] = temp_list[4]
                    temp_dict[temp_list[5]] = temp_list[6]
                    temp.append(temp_dict)
            elif flag > 1:
                temp = []
                data[each_line.strip().split()[1]] = temp
                flag = 1
                continue
    #查询相关的backend记录，并转换成字典作为函数返回值
    return data

def print_info(args,file='ha_proxy.conf'):
    """
    打印结果
    """
    data = query_info(args,file)
    if data.get(args) == None:
        print("配置文件中不存在该节点配置信息！")
    else:
        print('Name: %s'.center(30,'-') % args)
        for i in data.get(args):
            print(i)

def add_info(arg_site,arg_record):
    """
    定义一个函数，用于添加backend节点信息
    """
    flag = 0
    with open('ha_proxy.conf', 'r') as f1:
        for each_line in f1:
            if re.match('backend %s' % arg_site, each_line) != None:
                flag = 1
                break
	#没有找到backend的节点信息，添加节点
    if flag == 0:
        with open('ha_proxy.conf', 'r') as f1,open('ha_proxy_temp.conf','w') as f2:
            for each_line in f1:
                f2.write(each_line)
            f2.write('backend %s\n' % arg_site)
            f2.write('        %s\n' % arg_record)
	#找到backend的节点信息，添加下边的配置信息并临时写入'ha_proxy_temp.conf'
    else:
        with open('ha_proxy.conf','r') as f1,open('ha_proxy_temp.conf','w') as f2:
            for each_line in f1:
                if re.match('backend %s' % arg_site,each_line) != None:
                    f2.write(each_line)
                    f2.write('        %s\n' % arg_record)
                else:
                    f2.write(each_line)
	#将'ha_proxy_temp.conf'信息写回给'ha_proxy.conf'
    with open('ha_proxy.conf', 'w') as f1, open('ha_proxy_temp.conf', 'r') as f2:
        for each_line in f2:
            f1.write(each_line)


def del_info(arg_site,arg_record):
    """
    定义一个函数，用来删除指定节点的配置信息
    """
    data = query_info(arg_site)
    if data.get(arg_site) == None:
        print("配置文件中不存在该节点配置信息！")
    else:
        if data.get(arg_site).count(record_dict) == 0:
            print("配置文件中不存在该节点配置信息！")
        else:
            flag = 0
            with open('ha_proxy.conf', 'r') as f1:
                for each_line in f1:
                    if re.match('backend %s' % arg_site, each_line.strip()) != None:
                        flag = 1
			#将删除的结果写入到'ha_proxy_temp.conf'
            with open('ha_proxy.conf', 'r') as f1, open('ha_proxy_temp.conf', 'w') as f2:
                if flag == 1:
                    for each_line in f1:
                        if re.match(record, each_line.strip()) != None:
                            continue
                        else:
                            f2.write(each_line)
                else:
                    f2.write(each_line)
		#判断节点下面是否存在record记录，如果不存在，则连节点都删除并写回给文件'ha_proxy.conf'
        with open('ha_proxy.conf', 'w') as f1, open('ha_proxy_temp.conf', 'r') as f2:
            for each_line in f2:
                if query_info(arg_site,file='ha_proxy_temp.conf').get(arg_site) == None:
                    if re.match('backend %s' % arg_site, each_line.strip()):
                        continue
                    else:
                        f1.write(each_line)
                else:
                    f1.write(each_line)


while True:
    print(msg)
    num = input("请输入操作序号：")
    if num == '1':
        choose = input("输入您要查看的配置节点：").strip()
        print_info(choose)
        continue
    elif num == '2':
        choose = input("输入您要增加的配置节点：").strip()
        server_info = input("输入您要增加的配置server：").strip()
        weight_info = input("输入您要增加的配置weight：").strip()
        maxconn_info = input("输入您要增加的配置maxconn：").strip()
        record = 'server {0} {0} weight {1} maxconn {2}'.format(server_info,weight_info,maxconn_info)
        add_info(choose,record)
        print('配置添加成功!')
        print_info(choose)
    elif num == '3':
        choose = input("输入您要删除的配置节点：").strip()
        server_info = input("输入您要删除的配置server：").strip()
        weight_info = input("输入您要删除的配置weight：").strip()
        maxconn_info = input("输入您要删除的配置maxconn：").strip()
        record = 'server {0} {0} weight {1} maxconn {2}'.format(server_info, weight_info, maxconn_info)
        record_dict = {'server':'%s %s' %(server_info,server_info),'weight':weight_info,'maxconn':maxconn_info}
        del_info(choose, record)
        print('配置删除成功!')
    elif num == 'q':
        exit()
    else:
        print("无效输入，请重新选择！")