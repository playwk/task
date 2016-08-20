#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import paramiko

engine = create_engine("mysql+pymysql://root:python@12.12.11.140:3306/pylearn?charset=utf8", pool_size=5,
                       max_overflow=5)
Base = declarative_base()

result = engine.execute('show tables').fetchall()

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
    serline_id = Column(Integer, ForeignKey('serviceline.id'))


class Manager(ServiceLine, Host):

    def select(self, table, condition='default', method='default'):
        if method == 'filter_by':
            ret = session.query(table).filter_by(condition).all()
        else:
            ret = session.query(table).all()
        if
        print(ret)
        session.commit()

    def insert(self, table, info):
        session.add_all(info)
        self.select(table)

    def modify(self, table, condition, data):
        session.query(table).filter(condition).update(data)
        self.select(table)

    def remove(self, table, condition='default', method='default'):
        if method == 'filter_by':
            session.query(table).filter_by(condition).delete()
        else:
            session.query(table).delete()
        self.select(table)


ret = session.query(Host).all()
for i in ret:
    print(i.id)
