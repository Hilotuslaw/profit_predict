# -*- coding: UTF-8 -*-
# @FileName  :  req_resp_model.py
# @Time      :  2024/03/31 19:31:17
# @Author    :  Lotuslaw
# @Desc      :  request model and response model


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


from pydantic import BaseModel
from typing import List, Optional


class PredictRequest(BaseModel):
    config_name: str  # 配置人姓名
    config_time: str  # 配置时间, YYYY-mm-dd
    config_ip: str  # 配置人ip地址
    game: str  # 游戏名
    country: str  # 国家
    program_start_time: str  # 项目启动时间
    predict_start_time: str  # 预测起始日期
    history_dau: int  # 存量DAU
    predict_end_time: str  # 预测结束日期
    arr_month_history: List[str]  # 历史买量年月
    arr_date_history_real: List[int]  # 当月买量天数
    arr_month_install_rate: List[int]  # 当月买量占比
    predict_year_month: List[str]  # 预估年月
    arpu_in: List[float]  # 内购arpu
    arpu_ad: List[float]  # 广告arpu
    cpi: List[float]  # cpi
    cost_online_earning: List[float]  # 线上营销费用，比如网赚支出
    cost_market: List[float]  # 市场支出
    new_install: List[int]  # 日新增
    new_rule: List[float]  # 日新增规则
    day_n: List[int]  # 第N天
    re_rate: List[float]  # 留存率
    local_pay_ratio: float  # 本地支付占比
    local_pay_share_ratio: float  # 本地支付分成比例
    official_pay_share_ratio: float  # 官方支付分成比例
    cp_share_ratio: float  # CP分成比例
    fit_re_rate_method: bool  # 留存率拟合方式，false幂函数拟合，true修正幂函数拟合


class SubPredictResponse(BaseModel):
    format_date: List[str]  # 日度盈亏看板，日期
    date_serial: List[int]  # 日度盈亏看板，第N天
    new_install: List[int]  # 日度盈亏看板，日新增
    dau: List[int]  # 日度盈亏看板，DAU
    arpu_in: List[float]  # 日度盈亏看板，内购arpu
    arpu_ad: List[float]  # 日度盈亏看板，广告arpu
    official_income_aft_shared: List[int]  # 日度盈亏看板，分成后官方支付收入
    local_income_aft_shared: List[int]  # 日度盈亏看板，分成后本地支付收入
    income_in_aft_shared: List[int]  # 日度盈亏看板，总内购分成后
    income_ad: List[int]  # 日度盈亏看板，广告收入
    income_all: List[int]  # 日度盈亏看板，总流水
    income_all_cp_share: List[int]  # 日度盈亏看板，CP分成流水
    income_all_aft_shared: List[int]  # 日度盈亏看板，分成后总收入
    cpi: List[float]  # 日度盈亏看板，cpi
    cost_purchase: List[int]  # 日度盈亏看板，买量支出
    cost_online_earning: List[int]  # 日度盈亏看板，和预估时间区间匹配，线上营销费用，比如网赚支出
    cost_market: List[int]  # 日度盈亏看板，市场费用，和预估时间区间匹配
    profit_daily: List[int]  # 日度盈亏看板，每日盈亏
    profit_cumsum: List[int]  # 日度盈亏看板，累计盈亏
    format_month: List[str]  # 月度盈亏看板，月度
    new_install_month_avg: List[int]  # 月度盈亏看板，月度平均日新增
    dau_month_avg: List[int]  # 月度盈亏看板，月度平均DAU
    arpu_in_month: List[float]  # 月度盈亏看板，内购arpu
    arpu_ad_month: List[float]  # 月度盈亏看板，广告arpu
    official_income_aft_shared_month: List[int]  # 月度盈亏看板，分成后官方支付收入
    local_income_aft_shared_month: List[int]  # 月度盈亏看板，分成后本地支付收入
    income_in_aft_shared_month: List[int]  # 月度盈亏看板，总内购分成后
    income_ad_month: List[int]  # 月度盈亏看板,广告收入
    income_all_month: List[int]  # 月度盈亏看板，总流水
    income_all_cp_share_month: List[int]  # 月度盈亏看板，CP分成流水
    income_all_aft_shared_month: List[int]  # 月度盈亏看板，分成后总收入
    cpi_month: List[float]  # 月度盈亏看板，cpi
    cost_purchase_month: List[int]  # 月度盈亏看板，买量支出
    cost_online_earning_month: List[int]  # 月度盈亏看板，线上营销费用，比如网赚支出，和预估时间区间匹配
    cost_market_month: List[int]  # 月度盈亏看板，市场费用，和预估时间区间匹配
    profit_month: List[int]  # 月度盈亏看板，每月盈亏
    profit_cumsum_month: List[int]  # 月度盈亏看板，累计盈亏
    re_rate_pre_360: List[float]  # 拟合预测360日留存率
    lt_pre_360: List[float]  # 拟合预测360日LT


class PredictResponse(BaseModel):
    code: int
    message: str
    predict_response: Optional[SubPredictResponse] = None


class RePredictRequest(BaseModel):
    config_name: str  # 配置人姓名
    config_time: str  # 配置时间, YYYY-mm-dd HH:MM:SS
    config_ip: str  # 配置人ip地址
    game: str  # 游戏名
    country: str  # 国家
    program_start_time: str  # 项目启动时间
    predict_start_time: str  # 预测起始日期
    history_dau: int  # 存量DAU
    predict_end_time: str  # 预测结束日期
    arr_month_history: List[str]  # 历史买量年月
    arr_date_history_real: List[int]  # 当月买量天数
    arr_month_install_rate: List[int]  # 当月买量占比
    arpu_in: List[float]  # 内购arpu
    arpu_ad: List[float]  # 广告arpu
    cpi: List[float]  # cpi
    cost_online_earning: List[float]  # 线上营销费用，比如网赚支出
    cost_market: List[float]  # 市场支出
    new_install: List[int]  # 日新增
    day_n : List[int]  # 第N天
    re_rate: List[float]  # 留存率
    local_pay_ratio: float  # 本地支付占比
    local_pay_share_ratio: float  # 本地支付分成比例
    official_pay_share_ratio: float  # 官方支付分成比例
    cp_share_ratio: float  # CP分成比例
    fit_re_rate_method: bool  # 留存率拟合方式，false幂函数拟合，true修正幂函数拟合
