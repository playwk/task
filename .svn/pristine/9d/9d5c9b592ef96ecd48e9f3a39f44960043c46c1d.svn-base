#Author ZhengZhong,Jiang
#!/usr/bin/env python3
# -*- encoding = utf-8 -*-

status = 0
line_list = []
with open('nginx.conf.new','r',encoding='utf-8') as f1, open('nginx.conf.new2','w',encoding='utf-8') as f2:
        for line in f1:
            if line.strip() != 'location ~ .mp4{' and status != 1:
                f2.write(line)
            elif line.strip() == 'location ~ .mp4{' and status != 1:
                line_list.append(line)
                print(line_list)
                status = 1
            elif line.strip() != 'location ~ .mp4{' and status == 1:
                if line.strip() != '}':
                    line_list.append(line)
                else:
                    # space_num = len(line_list[1]) - len(line_list[1].strip())
                    space_num = line_list[1].count('\t')
                    line_list.append('\t' * space_num +
                                     'if ($request_uri ~* ^.*\/(.*)\.'
                                     '(doc|xls|docx|xlsx|ppt|pptx|rar|zip|apk|mp4|flv|txt|pdf)'
                                     '(\?n=([^&]+))$) {\n'
                                     )
                    line_list.append('\t' * (space_num + 1 ) +
                                     'add_headerContent - Disposition"attachment;$arg_n";\n'
                                     )
                    line_list.append('\t' * space_num + '}\n')
                    line_list.append(line)
                    for each_line in line_list:
                        f2.write(each_line)
                    status = 0

            else:
                f2.write(line)

