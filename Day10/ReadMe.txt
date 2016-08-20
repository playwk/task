ReadMe:

1.简易的ftp程序，支持用户注册，登录，文件上传下载，查看文件，切换目录，服务端记录用户操作日志等功能

2.支持命令，put 上传；get 下载； ls 查看目录； cd 切换目录；mkdir 创建目录

3.主要的目录及.py解释：

    bin/index.py 服务器程序启动入口

    conf/setting.py 程序有关的路径配置信息

    core/ftp_server.py ftp核心功能代码

    core/initialize.py ftp管理员用户初始化

    core/logged.py 日志功能

    db/user.db ftp账户信息

    upload/	所有用户数据文件的家目录

4.初始化管理员用户admin，密码：123456，默认所有注册用户磁盘配额200MB 

5.博客地址：http://www.cnblogs.com/sunjzz/p/5655135.html