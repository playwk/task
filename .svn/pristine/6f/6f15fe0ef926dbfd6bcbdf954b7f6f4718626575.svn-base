#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

import pika
import subprocess

conn = pika.BlockingConnection(pika.ConnectionParameters(host='12.12.11.140'))
chan = conn.channel()

chan.queue_declare(queue='rpc_queue')


def run(cmd):
    run_cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    run_info = run_cmd.stdout.read()

    if not len(run_info):
        run_info = run_cmd.stderr.read()
    if len(run_info) == 0:
        run_info = bytes("cmd has output", encoding='utf8')
    run_info=str(run_info, encoding='utf8')
    print(run_info)
    return run_info


def on_request(ch, method, props, body):
    print("[.] Run Command: %s" % body.decode())
    response = run(body.decode())

    ch.basic_publish(exchange='',
                     # 消息返回的队列路由
                     routing_key=props.reply_to,
                     # 封装消息ID，用于校验
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id, ),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

chan.basic_qos(prefetch_count=1)
chan.basic_consume(on_request, queue='rpc_queue')

print("[x] AWaiting RPC request")
chan.start_consuming()
