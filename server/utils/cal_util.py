# -*- coding: UTF-8 -*-
# @FileName  :  cal_util.py
# @Time      :  2024/03/31 22:04:14
# @Author    :  Lotuslaw
# @Desc      :  calculate utility.


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


import datetime
from typing import Tuple, List
from scipy.optimize import leastsq
import numpy as np


def cal_time_interval(program_start_time: datetime.datetime, 
                      predict_start_time: datetime.datetime, 
                      predict_end_time: datetime.datetime) -> Tuple:
    """
    将各个时段展开。

    :param program_start_time: 游戏项目启动时间
    :param predict_start_time: 预测起始日期
    :param predict_end_time: 预测结束日期
    :return: 展开后的各个时段。
    """
    days_history = [program_start_time.strftime('%Y-%m-%d')]
    days_predict = [predict_start_time.strftime('%Y-%m-%d')]
    time_tmp_1 = program_start_time
    if program_start_time == predict_start_time:
        days_history = []
    else:
        while True:
            if time_tmp_1 == predict_start_time - datetime.timedelta(days=1):
                break
            time_tmp_1 += datetime.timedelta(days=1)
            days_history.append(time_tmp_1.strftime('%Y-%m-%d'))
    
    time_tmp_2 = predict_start_time
    while True:
        time_tmp_2 += datetime.timedelta(days=1)
        days_predict.append(time_tmp_2.strftime('%Y-%m-%d'))
        if time_tmp_2 == predict_end_time:
            break
    return days_history, days_predict


def func_pow(x: float, p: float) -> float:
    """
    计算幂函数的结果。

    :param x: 输入值。
    :param p: 幂函数的参数(p_a, p_b)。
    :return: 幂函数的结果。
    """
    p_a, p_b = p
    return p_a * x ** p_b


def residuals_pow(p: Tuple[float, float], y: float, x: float) -> float:
    """
    计算幂函数的残差。

    :param p: 幂函数的参数(p_a, p_b)。
    :param y: 观测值。
    :param x: 幂函数的参数(p_a, p_b)。
    :return: 输入值。
    """
    ret = y - func_pow(x, p)
    return ret



def fit_re_rate(re_rate: List[float], x: List[int], p0: Tuple[float, float] = (0.5, 0.5)) -> np.ndarray:
    """
    对给定的留存率数据进行拟合，预测未来的留存率。

    :param re_rate: 留存率数据，通常为一组浮点数。
    :param x: 时间间隔列表，单位为天。
    :param p0: 幂函数的初始参数(p_a, p_b)。默认为(0.5, 0.5)。
    :return: 预测的留存率数组。
    """
    y = re_rate[1:]
    x = np.array([1, 3, 7, 14, 30, 45, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]) if x is None else x[1:]
    qs_pow = leastsq(residuals_pow, p0, args=(y, x))
    re_rate_pre = func_pow(np.arange(1, 10000), qs_pow[0])
    re_rate_pre = np.concatenate((np.array([1.0]), re_rate_pre))
    return re_rate_pre


def revise_re_rate(re_rate_pre_old: np.ndarray, y: List[float], x: List[float]) -> np.ndarray:
    """
    对给定的留存率数据进行修正。

    :param re_rate_pre_old: 之前拟合的留存率数组，通常为一组浮点数。
    :param y: 配置留存率数组，通常为一组浮点数。
    :param x: 配置留存率对应的时间间隔列表，单位为天。默认为None。
    :return: 修正的留存率数组。
    """
    ratio_config_predict = y[-1] / re_rate_pre_old[x[-1]]
    re_rate_pre = []
    ratio = None
    for i in range(10000):
        if i in x:
            re_rate_pre.append(y[x.index(i)])
            if i != x[-1]:
                ratio = None
            else:
                ratio = ratio_config_predict
        else:
            if ratio:
                if i < x[-1]:
                    re_rate_pre.append(re_rate_pre[-1] * ratio)
                else:
                    re_rate_pre.append(re_rate_pre_old[i] * ratio)
            else:
                x.append(i)
                x = sorted(x)
                index = x.index(i)
                front = x[index-1]
                back = x[index+1]
                ratio = (y[index] / y[index-1]) ** (1 / (back - front))
                re_rate_pre.append(re_rate_pre[i-1] * ratio)
                x.pop(index)
    return np.array(re_rate_pre)