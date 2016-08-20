### ReadME:

1. 主要使用linux平台vim开发

2. 支持用户选择主机组，然后选择主机组中主机登录

3. 文件目录说明：

   bin/Netconn.py	# 程序入口

   conf/config.py	# 相关配置参数，主要是数据库相关参数，数据库IP，数据库名，数据库端口，数据库用户名，密码，使用前，请先改写好相关配置数据。

   core/initdb.py	# 初始化数据库基本测试数据。确保数据库连接没有问题，进入目录下执行该脚本

   core/dropdb.py	#  删除数据库基本数据

   core/database.py	# 数据表的类定义，表结构可以参考ER图

   core/netconn.py	# 堡垒机主要的核心逻辑代码

4. 测试通过密码认证，无密码密钥登录，有密码密钥登录



博客地址：http://www.cnblogs.com/sunjzz/p/5743193.html