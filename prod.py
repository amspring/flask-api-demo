# -*- coding: utf-8 -*-
# File     : gunicorn.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-08-04 09:54
# Remarks  :
# import gevent
from gevent import monkey

monkey.patch_all()

import multiprocessing
from app.conf import settings

# 监听内网端口
bind = f"{settings.app.host}:{settings.app.port}"

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程开启的线程数
threads = 2

# 监听队列
backlog = 2048

# 工作模式协程。
# worker_class = "gevent"
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

# 设置守护进程,将进程交给supervisor管理
daemon = 'false'

# worker_connections最大客户端并发数量，默认情况下这个值为1000。
worker_connections = 2048

# 设置日志记录水平
loglevel = 'info'

x_forwarded_for_header = 'X-FORWARDED-FOR'
