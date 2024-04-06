# -*- coding: UTF-8 -*-
# @FileName  :  log_util.py
# @Time      :  2024/03/31 17:28:19
# @Author    :  Lotuslaw
# @Desc      :  log utility.


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


import logging
from logging.handlers import TimedRotatingFileHandler


formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [%(levelname)s] [%(thread)d] - %(message)s')
handler = TimedRotatingFileHandler(
    './logs/flask.log',
    when='D',
    interval=1,
    backupCount=30,
    encoding='UTF-8',
    delay=False,
    utc=False
)
handler.setLevel(logging.WARNING)
handler.setFormatter(formatter)
