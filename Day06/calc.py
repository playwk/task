#Author ZhengZhong,Jiang
import re

def func_1(args):
    """
    计算加减
    :param args:
    :return:
    """
    #对重复出现的‘--’符号做‘+’转换
    args = re.sub('\-{2}', '+', args)
    args = re.sub('\+\-', '-', args)
    #以加减号分割表达式
    data = re.split("([\+\-])", args.strip("()"))
    #对列表只有一个元素的直接返回列表值
    if len(data) == 1:
        return args
    else:
        #按照运算符的优先级，加减法是最后计算，因此try计算表达式
        try:
            for i in range(data.count('')):
                data[data.index('')] = '0'
            if data[1] == '-':
                res = float(data[0]) - float(data[2])
            else:
                res = float(data[0]) + float(data[2])
            for i in range(2, len(data)-2, 2):
                if data[i+1] == '-':
                    res -= float(data[i+2])
                else:
                    res += float(data[i+2])
            return res
        #抓捕异常，加减法不能进行的表达式一定不合法！
        except:
            print("表达式不合法！请重新输入!")
            return 1


def func_2(args):
    """
    计算乘除
    :param args:
    :return:
    """
    data = re.split('([\*\/])', args)
    if data[1] == '*':
        res = float(data[0]) * float(data[2])
    else:
        res = float(data[0]) / float(data[2])
    for i in range(2, len(data)-2, 2):
        if data[i+1] == '*':
            res *= float(data[i+2])
        else:
            res /= float(data[i+2])
    return res


def func_3(args):
    """
    处理表达式中运算符变换
    :param args:
    :return:
    """
    data = ''.join(args)
    if re.search('[\*\/]\-', data):
        for i in range(len(args)):
            if re.match('[\*]\-', args[i]):
                args[i-2] = args[i-2] + '-'
                args[i] = '*'
            if re.match('[\/]\-', args[i]):
                args[i - 2] = args[i - 2] + '-'
                args[i] = '/'
        for i in range(len(args)):
            args[i] = re.sub('\+\-', '-', args[i])
            args[i] = re.sub('\-\-', '+', args[i])
        return func_3(args)
    else:
        for i in range(len(args)):
            args[i] = re.sub('\+\-', '-', args[i])
            args[i] = re.sub('\-\-', '+', args[i])
        return ''.join(args)


def func_4(args):
    """
    四则混合运算
    :param args:
    :return:
    """
    # print(args)
    # 处理表达式中运算符
    args = re.sub('\+\-', '-', args)
    args = re.sub('\*\+', '*', args)
    args = re.sub('\/\+', '/', args)
    args = re.sub('\*\+', '*', args)
    data = re.split("([0-9]+\.?[0-9]*)", args)
    for i in range(data.count('')):
        data.remove('')
    res = func_3(data)
    data = re.split('([\+\-])', res)
    res = []
    for i in data:
        try:
            result = func_2(i)
            res.append(str(result))
        except:
            res.append(i)
    return func_1(''.join(res))


def func(args):
    """
    处理表达式中括号
    :param args:
    :return:
    """
    result = []
    if re.search("\([0-9\+\-\*\/\.]+\)", args):
        data = re.split("(\([0-9\+\-\*\/\.]+\))", args)
        for i in data:
            if re.match("(\([0-9\+\-\*\/\.]+\))", i):
                res = func_4(i.strip('()'))
                result.append(str(res))
            else:
                    result.append(i)
        return func(''.join(result))
    else:
        return func_4(''.join(args))


if __name__ == '__main__':
    while True:
        data = input("请输入要计算的表达式：")
        res = func(data)
        if res != 1:
            print(res)
            break
