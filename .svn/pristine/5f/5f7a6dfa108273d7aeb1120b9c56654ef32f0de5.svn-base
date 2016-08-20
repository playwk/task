#Author ZhengZhong,Jiang

info = {'beijing':
            {'haidian': ['xierqi', 'wudaokou'],
             'changping': ['shahe', 'huoying']},
        'shenzhen':
            {'luohu': ['guomao', 'laojie'],
             'futian': ['xiangmihu', 'chegongmiao']}
        }

record = []
flag = True
#打印一级菜单，并将目录关键字存放到record有序列表，记录用户选择
# 进入程序第一次打印菜单，并只对第一次选择进行处理
while flag:
    area = []
    for i in info.keys():
        area.append(i)
    for x, y in enumerate(area):
        print('%s.%s' % (x, y))
    print('输入菜单名选择进入，输入b/B返回上级菜单，输入q/Q退出')
    choose = input('输入选择: ')
    if choose in area:
        record.append(choose)
        flag = False
    elif choose == 'q' or choose == 'Q':
        exit()
    elif choose == 'b' or choose == 'B':
        continue
    #无效菜单名提示
    else:
        print('请输入正确的菜单名')
        continue
#对进入到第二级菜单之后的所有操作进行处理
flag = True
while flag:
    site = info
    tag = record
    for i in range(len(record)):
        site = site[tag[i]]
    for m,n in enumerate(site):
        print('%s.%s' % (m, n))
    choose = input('输入选择: ')
    if choose == 'b' or choose == 'B':
        # 退到一级菜单后不再继续
        if len(record) > 0:
            record.pop()
    elif choose == 'q' or choose == 'Q':
        exit()
    elif choose in site:
        #展示三级菜单后不再继续
        if len(record) < 2:
            record.append(choose)
    #无效菜单名提示
    else:
        print('请输入正确的菜单名')
