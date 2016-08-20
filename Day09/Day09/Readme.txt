---------------------------Start--------------------------------------
Version:    1.0
Date   :    2016-07
Author :    Liujiang
Email  ：   feixuelym@sina.com
Github :    http://github.com/feixuelove1009
Blog   ：   python网络编程socket （一）
                http://www.cnblogs.com/feixuelove1009/p/5647692.html
            TCP/IP协议（一）
                http://www.cnblogs.com/feixuelove1009/p/5647259.html
Python:     3.5.1

function:
    这是一个基于socketserver的FTP软件，分客户端和服务端两个部分，实现了
cd/dir/ls/mkdir/du/get/put/help等核心命令。主要功能如下：

    1. 用户密码采用MD5加密认证；
    2. 允许多用户同时登录；
    3. 每个用户有自己的家目录 ，且只能访问自己的家目录；
    4. 用户可以查看家目录内的文件；
    5. 用户可以在家目录内随意切换目录；
    6. 对用户进行了磁盘配额，每个用户的可用空间不同；
    7. 可上传和下载文件，并进行MD5值校验，保证文件一致性；
    8. 文件传输过程中显示进度条；
    9. 支持文件的断点续传！
    10. 一个附加的服务器后台管理程序，用于添加、删除用户，修改用户密码和限额
----------------------------End----------------------------------------

一、文件目录结构：

day09
FTP程序
│  Readme.txt                       # 帮助文件
│
├─MyFtp_client                      # ftp客户端
│  │  __init__.py
│  │
│  ├─bin
│  │      MyFtp_client.py           # 客户端启动模块
│  │      __init__.py
│  │
│  ├─conf
│  │  │  settings.py                # 客户端配置文件
│  │  │  __init__.py
│  │
│  ├─modules                        # 模块目录
│  │  │  client_argv_handler.py     # 客户端执行参数解析模块
│  │  │  MyFtp_client_core.py       # 客户端核心逻辑模块
│  │  │  __init__.py
│  │
│  └─var                            # ftp空间
│      │  __init__.py
│      │
│      └─users                      # 用户空间
│          │  __init__.py
│          │
│          └─alex                   # 用户alex的家目录
│              │
│              └─.tmp               # 临时文件存放目录

└─MyFtp_server                       # ftp服务器
    │  __init__.py
    │
    ├─bin
    │      MyFtp_server.py            # 服务器端启动文件
    │      __init__.py
    │
    ├─conf
    │  │  settings.py                # 服务器配置文件
    │  │  __init__.py
    │  │
    ├─db
    │      user.json                  # ftp用户信息文件
    │
    ├─modules
    │  │  manage_core.py             # 服务器后台管理模块
    │  │  MyFtp_server_core.py       # 服务器核心逻辑模块
    │  │  server_argv_handler.py     # 服务器运行参数处理模块
    │  │  __init__.py
    │  │
    │
    └─var
        └─users                     # 在服务器上的用户家目录
            ├─alex                  # alex的家目录
            │  ├─.tmp              # alex的临时文件存储目录
            └─jack                  # jack的家目录
                └─.tmp              # jack的临时文件存储目录

二、数据结构

        位于服务器端的db目录下的user.json文件保存了ftp用户的账户信息。这是一个字典类型
    的json数据，每一个键值对是这样的：
        用户名：{密码：md5值，磁盘限额：2}


三、测试用例：

    用户1：alex   密码：123
    用户2：jack   密码：123

    测试文件：   MyFtp_client/bin目录下的test3.jpg  6.3MB
                 由于svn的原因，麻烦助教老师自行准备大型文件用于测试。
                 也可以使用本机上的其他文件进行测试。

    断点续传的测试：在传输过程中手动停止服务器或客户端程序，再启动并登陆

四、使用说明

    代码是在windows的pycharm环境中进行编写和测试的。

    服务器ip_port=("0.0.0.0",6666)

        python3 MyFtp_server.py start      启动FTP服务器
        python3 MyFtp_server.py manage     启动FTP后台管理程序

    客户端连接服务器时，请务必先查询当前服务器的ip地址，端口请使用6666

        python3 MyFtp_client.py xxx.xxx.xxx.xxx:6666  启动FTP客户端

        注意：使用冒号连接ip和端口,客户端可同时开启多个。


    （1）ftp服务器运行期间
         提供了一定的信息提示，包括客户端断开连接、上传下载md5码等

    （2）ftp服务器后台管理程序
         用于添加、删除用户，修改用户密码和磁盘限额

    （3）ftp客户端功能说明

            1. 登录：   客户端启动后需要立刻登录，三次错误退出，成功则显示提示符
                        [alex@192.168.1.100 \] ftp>
                        格式：[用户名@服务器ip 当前路径] ftp>
                        当前路径会随着cd命令的变化而变化

            2. dir：     查看目录，“/”代表用户家目录，可使用类似/test/test2/test3的绝对路径，
                         也可以使用../../test之类的相对路径。但是系统内部会判断路径是否处于用户
                         家目录内，如果不是，则提示路径错误。

            3. ls:       dir命令的复用

            4. cd：      路径切换，可使用绝对路径和相对路径，并限制在用户家目录内

            5. du：      查看用户磁盘限额，每次上传文件时进行空间容量判断，不足则不允许上传

            6. mkdir：   新建目录，可使用绝对路径和相对路径，并自动判断路径的正确与否，是否在
                         家目录内。由于平台的原因，暂不支持多级递归建立。

            7. get：     下载文件，可以get xxx或get xxx  yyy，自动判断绝对路径和相对路径，自动
                         判断文件是否存在，自动判断文件名的变化。

            8. put：     上传文件，可以put xxx或put xxx  yyy，自动判断绝对路径和相对路径，自动
                         判断文件是否存在，自动判断文件名的变化。

            9. 断点续传： 每次上传和下载文件时，在用户的家目录的.tmp文件夹内，建立一个以文件
                          MD5值为名的临时文件。正常任务完成时，将该文件复制到目标文件，并删除
                          该临时文件。当任务中途中断后，再继续执行该任务时，通过MD5值判断是否
                          有曾经传输过的临时文件，如果有，就从上次传输的后面继续传。

            10.进度条显示： 通过对比已经传输的文件大小和总的文件大小，动态显示传输百分比。

            11. help：       帮助文档

五、程序使用示例

（1）登录：

    -----欢迎使用MyFtp-----
    请输入用户名：  alex
    请输入密码：  123
    200 登录成功
    [alex@192.168.1.100 \] ftp>

（2）dir:

    [alex@192.168.1.100 \] ftp> dir
    \ 的目录
    .tmp						<DIR>
    test						<DIR>
    [alex@192.168.1.100 \] ftp> dir /test
    \ 的目录
    test2						<DIR>
    [alex@192.168.1.100 \] ftp>

(3)ls：

    [alex@192.168.1.100 \] ftp> ls
    \ 的目录
    .tmp						<DIR>
    test						<DIR>
    [alex@192.168.1.100 \] ftp> ls /test/test2
    \ 的目录
    test3						<DIR>
    [alex@192.168.1.100 \] ftp>

(4)cd:

    [alex@192.168.1.100 \] ftp> cd
    [alex@192.168.1.100 \] ftp> cd ..
    401 路径错误
    [alex@192.168.1.100 \] ftp> cd /test/test2
    [alex@192.168.1.100 \test\test2] ftp> dir
    \test\test2 的目录
    test3						<DIR>
    [alex@192.168.1.100 \test\test2] ftp> cd ..
    [alex@192.168.1.100 \test] ftp>

（5）du:

    [alex@192.168.1.100 \test] ftp> du
    当前已用空间：0.00 MB
    当前可用空间：2048.00 MB
    用户磁盘限额： 2GB
    [alex@192.168.1.100 \test] ftp>

(6)mkdir:

    [alex@192.168.1.100 \test] ftp> mkdir 123
    308 目录建立成功!
    [alex@192.168.1.100 \test] ftp> dir
    \test 的目录
    123						<DIR>
    test2						<DIR>
    [alex@192.168.1.100 \test] ftp>

(7)put:

    [alex@192.168.1.100 \test] ftp> put f:\15.avi
    MD5校验码为：a3abcadb886888d5f81a60549ecbe101
    任务进度：[#########################]100%
    文件传输成功，一致性校验通过!
    [alex@192.168.1.100 \test] ftp>

(8)get：

    [alex@192.168.1.100 \] ftp> get test3.jpg
    目标文件已存在，覆盖yes，任意键取消！yes
    任务进度：[#########################]100%
    MD5校验码为：1d6fad42daa8c17dd92c4d5dd6ec36ad
    文件传输成功，一致性校验通过!
    [alex@192.168.1.100 \] ftp>

(9)断点续传：

    [alex@192.168.1.100 \test] ftp> get 15.avi g:\33.avi
    任务进度：[#######                  ]29%
    Process finished with exit code -1
    [alex@192.168.1.100 \] ftp> cd test
    [alex@192.168.1.100 \test] ftp> dir
    \test 的目录
    123						<DIR>
    15.avi		262.41MB
    test2						<DIR>
    [alex@192.168.1.100 \test] ftp> get 15.avi g:\33.avi
    发现未完成的下载任务，自动续传！
    任务进度：[#########################]100%
    MD5校验码为：a3abcadb886888d5f81a60549ecbe101
    文件传输成功，一致性校验通过!
    [alex@192.168.1.100 \test] ftp>

(10)help:

    [alex@192.168.1.100 \] ftp> help

    【帮助信息】：
        可执行命令：
        dir：     查看目录内容
        ls：      查看目录内容
        cd：      切换目录
        mkdir：   新建目录（因为平台的原因，暂不支持递归建立）
        du：      查看用户当前已用磁盘容量
        get：     下载文件
        put：     上传文件
        help:     查看帮助文件