#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

import database


if __name__ == "__main__":
    database.Base.metadata.create_all(database.engine)
    database.session.add_all([database.BUsers(b_username='jzz',),])
    database.session.commit()
    database.session.add_all([
        database.Groups(group_name='oldboy'),
        database.Groups(group_name='edustar')
        ])
    database.session.commit()
    database.session.add_all([
        database.Hosts(host_name='oldboy',host_ip='127.0.0.1',host_port='22'),
        database.Hosts(host_name='oldboy',host_ip='192.168.8.5',host_port='22'),
        database.Hosts(host_name='edustar',host_ip='127.0.0.1',host_port='22'),
        database.Hosts(host_name='edustar',host_ip='192.168.8.5',host_port='22'),
        ])
    database.session.commit()
    database.session.add_all([
        database.GroupHost(group_id=1,host_id=1),
        database.GroupHost(group_id=1,host_id=2),
        database.GroupHost(group_id=2,host_id=1),
        database.GroupHost(group_id=2,host_id=2)
        ])
    database.session.commit()
    database.session.add_all([
        database.Users(username='jiang',password='123456',usercert='/home/jiang/.ssh/id_rsa',certpass=''),
        database.Users(username='chen',password='123456',usercert='/home/chen/.ssh/id_rsa',certpass='python')
        ])
    database.session.commit()
    database.session.add_all([
        database.BUserGroup(b_user_id=1, group_id=1),
        database.BUserGroup(b_user_id=1, group_id=2)
        ])
    database.session.commit()
    database.session.add_all([
        database.GroupHost(group_id=1, host_id=1),
        database.GroupHost(group_id=2, host_id=2),
        ])
    database.session.commit()
    database.session.add_all([
        database.HostUser(host_id=1, user_id=1),
        database.HostUser(host_id=1, user_id=2),
        database.HostUser(host_id=2, user_id=1),
        database.HostUser(host_id=2, user_id=2),
        ])
    database.session.commit()
