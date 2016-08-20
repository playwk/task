#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import paramiko

#远程执行命令
def run_command(cmd, host, user_name, pass_word, port=22):
    transport = paramiko.Transport(host, port)
    transport.connect(username=user_name, password=pass_word)

    ssh = paramiko.SSHClient()
    ssh._transport = transport

    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(str(stdout.read(),encoding='utf8'))

    transport.close()


engine = create_engine("mysql+pymysql://root:python@12.12.11.137:3306/pylearn?charset=utf8", pool_size=5,
                       max_overflow=5)
Base = declarative_base()

table_name = engine.execute('show tables').fetchall()

Session = sessionmaker(bind=engine)
session = Session()

class ServiceLine(Base):
    __tablename__ = 'serviceline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    serline_name = Column(String(50))


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostip = Column(String(20))
    hostname = Column(String(50))
    login_user = Column(String(50))
    login_pawd = Column(String(50))
    login_port = Column(Integer)
    serline_id = Column(Integer, ForeignKey('serviceline.id'))


class Manager(ServiceLine, Host):
    def __init__(self, table):
        self.table = table
        column = engine.execute('desc %s' % self.table).fetchall()
        if table == 'host':
            self.class_name = 'Host'
            self.obj = Host
        elif table == 'serviceline':
            self.class_name = 'ServiceLine'
            self.obj = ServiceLine
        column_list = []
        for i in column:
            column_list.append('%s' % i[0])
        self.table_column = column_list

    # 主机有关信息的读取
    def queryhost(self, ip):
        ret = session.query(Host.id, Host.hostip, Host.hostname,
                            Host.login_user,
                            Host.login_pawd,
                            Host.login_port,
                            Host.serline_id).filter_by(hostip=ip).all()
        self.login_user = ret[0][3]
        self.login_pawd = ret[0][4]
        self.login_port = ret[0][5]

    # 查询主机和业务对应关系信息
    def select(self):
        if self.obj == Host:
            ret = session.query(Host.id, Host.hostip, Host.hostname,
                                Host.login_user,
                                Host.login_pawd,
                                Host.login_port,
                                Host.serline_id).all()
        else:
            ret = session.query(ServiceLine.id,
                                ServiceLine.serline_name).all()
        for line in ret:
            print(line)
        session.commit()

    # 仅支持一次单条数据添加
    def insert(self, info):
        try:
            if info[0] == 'Host':
                session.add_all([Host(hostip=info[1],
                                      hostname=info[2],
                                      login_user=info[3],
                                      login_pawd=info[4],
                                      login_port=int(info[5]),
                                      serline_id=int(info[6]),
                                      )])
            elif info[0] == 'ServiceLine':
                session.add_all([ServiceLine(serline_name=info[1], )])
            session.commit()
        except:
            print("raise a error! ")
        self.select()

    # 仅支持主键ID大于某值的批量删除
    def remove(self, condition):
        if self.obj == Host:
            session.query(Host).filter(Host.id>int(condition)).delete()
        else:
            session.query(ServiceLine).filter(ServiceLine.id>int(condition)).delete()
        self.select()

    # 初始化库表
    @staticmethod
    def init_table():
        Base.metadata.create_all(engine)

    # 删除库表
    @staticmethod
    def drop_table():
        Base.metadata.drop_all(engine)

# Manager.drop_table()
# Manager.init_table()