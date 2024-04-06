# -*- coding: UTF-8 -*-
# @FileName  :  gunicorn.py
# @Time      :  2024/04/05 12:45:03
# @Author    :  Lotuslaw
# @Desc      :  gunicorn config.


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


import multiprocessing


# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 监听内网端口5000
bind = '0.0.0.0:5000'

# 设置守护进行，将进程交由supervisor管理
daemon = 'false'

# 工作模式设置为协程
worker_class = 'sync'

# 设置进程文件目录
pidfile = '/tmp/gunicorn.pid'

# 禁用keepalive
keepalive = 0

# 设置访问日志和错误信息日志路径
accesslog = './logs/gunicorn_access.log'
errorlog = './logs/gunicorn_error.log'

# 设置日志记录水平
loglevel = 'warning'
