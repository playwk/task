# Auther: ZhengZhong,Jiang

def fetch(node):
    result = []
    with open('ha_proxy.conf','r') as f:
        flag = False
        for line in f:
            if line.strip().startswith('backend') and line.strip() == 'backend ' + node:
                flag = True
                continue
            if flag and line.strip().startswith('backend'):
                flag = False
                break
            if flag and line.strip():
                result.append(line)
    print(result)


def add(backend, record):
    # 思路一：
    # 思路二：
    # 先检查记录存不存
    record_list = fetch(backend)
    if not record_list:
        # backend不存在
        with open('ha.conf', 'r') as old, open("new.conf", 'w') as new:
            for line in old:
                new.write(line)
            new.write("\nbackend " + backend + "\n")
            new.write(" " * 8 + record + "\n")
    else:
        # backend存在
        if record in record_list:
            # record已经存在
            # import shutil
            # shutil.copy("ha.conf", 'new.conf')
            pass
        else:
            # backend存在,record不存在
            record_list.append(record)
            with open('ha.conf', 'r') as old, open('new.conf', 'w') as new:
                flag = False
                for line in old:
                    if line.strip().startswith("backend") and line.strip() == "backend " + backend:
                        flag = True
                        new.write(line)
                        for new_line in record_list:
                            new.write(" "*8 + new_line + "\n" )
                    if flag and line.strip().startswith("backend"):
                        flag = False
                        new.write(line)
                        continue
                    if line.strip() and not flag:
                        new.write(line)



fetch('buy.oldboy.org')
