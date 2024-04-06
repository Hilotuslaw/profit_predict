# -*- coding: UTF-8 -*-
# @FileName  :  views_predict.py
# @Time      :  2024/03/31 17:19:23
# @Author    :  Lotuslaw
# @Desc      :  origin predict


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


import pandas as pd
import numpy as np
from flask import current_app, views
from flask_pydantic import validate
import json
import datetime
from models.req_resp_model import PredictRequest, PredictResponse, SubPredictResponse
from utils.cal_util import cal_time_interval, fit_re_rate, revise_re_rate
from http import HTTPStatus


class PredictView(views.MethodView):
    @validate()
    def post(self, body: PredictRequest) -> PredictResponse:
        # TODO 参数解析
        config_name = body.config_name
        config_time = body.config_time
        config_ip = body.config_ip
        game = body.game
        country = body.country
        program_start_time = body.program_start_time
        predict_start_time = body.predict_start_time
        history_dau = body.history_dau
        predict_end_time = body.predict_end_time
        arr_month_history = body.arr_month_history
        arr_date_history_real = body.arr_date_history_real
        arr_month_install_rate = body.arr_month_install_rate
        predict_year_month = body.predict_year_month
        arpu_in = body.arpu_in
        arpu_ad = body.arpu_ad
        cpi = body.cpi
        cost_online_earning = body.cost_online_earning
        cost_market = body.cost_market
        new_install = body.new_install
        new_rule = body.new_rule
        day_n = body.day_n
        re_rate = body.re_rate
        local_pay_ratio = body.local_pay_ratio
        local_pay_share_ratio = body.local_pay_share_ratio
        official_pay_share_ratio = body.official_pay_share_ratio
        cp_share_ratio = body.cp_share_ratio
        fit_re_rate_method = body.fit_re_rate_method

        # TODO 计算确认时间区间
        start_time = datetime.datetime.strptime(program_start_time, '%Y-%m-%d')
        predict_start_time = datetime.datetime.strptime(predict_start_time, '%Y-%m-%d')
        predict_end_time = datetime.datetime.strptime(predict_end_time, '%Y-%m-%d')
        days_history, days_predict = cal_time_interval(start_time, predict_start_time, predict_end_time)

        # TODO 计算按照时间区间展开的arpu_in,arpu_ad,cpi,online_earning,cost_market
        # 根据配置的预测年月，获取对应年月的数据，days_predict_list计算每个月份的天数
        days_predict_list = []
        for mon in predict_year_month:
            days_predict_list.append(sum([x[:7] == mon for x in days_predict]))
        arpu_in_res = []
        arpu_ad_res = []
        cpi_res = []
        cost_online_earning_res = []
        cost_market_res = []
        new_install_res = []
        for i, days in enumerate(days_predict_list):
            arpu_in_res += [arpu_in[i]] * days
            arpu_ad_res += [arpu_ad[i]] * days
            cpi_res += [cpi[i]] * days
            cost_online_earning_res += [cost_online_earning[i]] * days
            cost_market_res += [cost_market[i] / days] * days
            new_rule_res = np.array([new_rule[i]] * days).cumprod()
            new_install_res += list(new_install[i] * new_rule_res)

        # TODO 拟合留存率曲线，根据预测留存率，计算历史每日买量，计算预测DAU
        y = np.array(re_rate)
        x = np.array(day_n)
        re_rate_pre = fit_re_rate(y, x)
        if fit_re_rate_method:
            re_rate_pre = revise_re_rate(re_rate_pre, y.tolist(), x.tolist())
        re_rate_pre_360 = np.round(re_rate_pre[:361], 4)
        lt_pre_360 = np.round(re_rate_pre_360.cumsum(), 4)

        # TODO 预测未来买量的留存
        dau_list = []
        for i, install in enumerate(new_install_res):
            retention = install * re_rate_pre
            retention = list(np.concatenate((np.array([0.0] * i), retention))[:5000])
            dau_list.append(retention)

        # TODO 判断历史买量天数是否为0以及历史买量是否为0，如果不为0，计算历史买量在后续的留存
        if program_start_time == predict_start_time or history_dau == 0:
            pass
        else:
            # 搜索历史每日买量
            coefficient_compute = []  # 计算系数
            for i, install_rate in enumerate(arr_month_install_rate):
                if i == 0:
                    coefficient_compute.append(1)
                else:
                    coefficient_compute.append(install_rate / arr_month_install_rate[0] * arr_date_history_real[0] / arr_date_history_real[i])
            # 历史买量在预测首日对应的留存率
            re_rate_history = [re_rate_pre[len(days_history)-i] for i in range(len(days_history))]
            days_history_list = []
            for mon in arr_month_history:
                days_history_list.append(sum([x[:7] == mon for x in days_history]))
            if len(days_history_list) == 1:
                re_rate_history_list = [sum(re_rate_history)]  # 一整月的买量在预测日的留存率求和，假设每日买量相同
            else:
                days_history_list_modify = np.array([0] + days_history_list).cumsum()  # 按月展开，因为每月计算系数不同
                re_rate_history_list = [sum(re_rate_history[days_history_list_modify[i]: days_history_list_modify[i+1]]) for i in range(len(days_history_list_modify)-1)]
            # 搜索哪个买量值损失最小
            arr_test_install = np.arange(1, 100001)
            arr_loss = np.abs(arr_test_install * ((np.array(coefficient_compute) * np.array(re_rate_history_list)).sum()) - history_dau)
            history_install_day = np.argmin(arr_loss) + 1
            history_install_list = []
            # 历史每个月中每一天的安装
            for i, days in enumerate(days_history_list):
                history_install_list += [history_install_day * coefficient_compute[i]] * days
            # 历史买量在预测日的留存
            for i, install in enumerate(history_install_list):
                retention = list((install * re_rate_pre[(len(history_install_list) - i):])[:5000])
                dau_list.append(retention)
        dau_res = np.round(np.array(dau_list).sum(axis=0), 0)[:len(days_predict)]

        # TODO 重新组装DataFrame，计算对应盈亏
        official_income_after_share = np.round(dau_res * np.array(arpu_in_res) * (1 - local_pay_ratio) * (1 - official_pay_share_ratio), 0).astype(np.float32)
        local_income_after_share = np.round(dau_res * np.array(arpu_in_res) * local_pay_ratio * (1 - local_pay_share_ratio), 0).astype(np.float32)
        df_profit_day = pd.DataFrame(
            data=[
                np.array(days_predict),  # 日期
                np.arange(1, len(days_predict) + 1),  # 第N天
                np.array(new_install_res),  # 日新增
                dau_res,  # DAU
                np.array(arpu_in_res),  # 内购arpu
                np.array(arpu_ad_res),  # 广告arpu
                np.round(official_income_after_share),  # 分成后官方支付收入
                np.round(local_income_after_share),  # 分成后本地支付收入
                np.round(official_income_after_share + local_income_after_share, 0),  # 分成后总内购收入
                np.round(dau_res * np.array(arpu_ad_res), 0),  # 广告收入
                np.round(dau_res * np.array(arpu_ad_res) + dau_res * np.array(arpu_in_res), 0),  # 总流水
                np.round((dau_res * np.array(arpu_ad_res) + dau_res * np.array(arpu_in_res)) * cp_share_ratio, 0),  # CP分成流水
                np.round(official_income_after_share + local_income_after_share + dau_res * np.array(arpu_ad_res), 0),  # 分成后总收入
                np.array(cpi_res),  # CPI
                np.round(np.array(cpi_res) * np.array(new_install_res), 0),  # 投放支出
                np.round(np.array(cost_online_earning_res), 0),  # 网赚支出
                np.round(np.array(cost_market_res), 0),  # 市场支出
                np.round(official_income_after_share + local_income_after_share + dau_res * np.array(arpu_ad_res) - np.array(cpi_res) * np.array(new_install_res) - \
                         np.array(cost_online_earning_res) - np.array(cost_market_res) - (dau_res * (np.array(arpu_in_res) + np.array(arpu_ad_res))) * cp_share_ratio, 0),  # 每日盈亏
                np.round((official_income_after_share + local_income_after_share + dau_res * np.array(arpu_ad_res) - np.array(cpi_res) * np.array(new_install_res) - \
                          np.array(cost_online_earning_res) - np.array(cost_market_res) - (dau_res * (np.array(np.array(arpu_in_res) + np.array(arpu_ad_res)))) * cp_share_ratio).cumsum(), 0)  # 累计盈亏
            ]
        )
        df_profit_day = df_profit_day.T
        df_profit_day.columns = [
            'format_date', 'date_serial', 'new_install', 'dau', 'arpu_in', 'arpu_ad', 'official_income_aft_share',
            'local_income_aft_share', 'income_in_aft_share', 'income_ad', 'income_all', 'income_all_cp_share', 'income_all_aft_shared',
            'cpi', 'cost_purchase', 'cost_online_earning', 'cost_market', 'profit_day', 'profit_cumsum'
        ]

        # 月度
        df_profit_month_tmp = df_profit_day.copy()
        df_profit_month_tmp['format_month'] = df_profit_month_tmp['format_date'].apply(lambda x: x[:7])
        data_profit_month = []
        for fmonth in df_profit_month_tmp['format_month'].unique():
            data_tmp = [fmonth]
            df_tmp = df_profit_month_tmp[df_profit_month_tmp['format_month'] == fmonth]
            data_tmp.append(round(df_tmp['new_install'].astype(np.float32).astype(int).mean(), 0))
            data_tmp.append(round(df_tmp['dau'].mean(), 0))
            data_tmp.append(round(df_tmp['arpu_in'].mean(), 3))
            data_tmp.append(round(df_tmp['arpu_ad'].mean(), 3))
            data_tmp.append(round(df_tmp['official_income_aft_share'].sum(), 0))
            data_tmp.append(round(df_tmp['local_income_aft_share'].sum(), 0))
            data_tmp.append(round(df_tmp['income_in_aft_share'].sum(), 0))
            data_tmp.append(round(df_tmp['income_ad'].sum(), 0))
            data_tmp.append(round(df_tmp['income_all'].sum(), 0))
            data_tmp.append(round(df_tmp['income_all_cp_share'].sum(), 0))
            data_tmp.append(round(df_tmp['income_all_aft_shared'].sum(), 0))
            data_tmp.append(round(df_tmp['cpi'].astype(np.float32).mean(), 3))
            data_tmp.append(round(df_tmp['cost_purchase'].astype(np.float32).sum(), 0))
            data_tmp.append(round(df_tmp['cost_online_earning'].astype(np.float32).sum(), 0))
            data_tmp.append(round(df_tmp['cost_market'].astype(np.float32).sum(), 0))
            data_tmp.append(round(df_tmp['profit_day'].sum(), 0))
            data_profit_month.append(data_tmp)
        df_profit_month = pd.DataFrame(data_profit_month, columns=[
            'format_month', 'new_install_month_avg', 'dau_month_avg', 'arpu_in_month', 'arpu_ad_month', 'official_income_aft_shared_month',
            'local_income_aft_shared_month', 'income_in_aft_shared_month', 'income_ad_month', 'income_all_month', 'income_all_cp_share_month', 'income_all_aft_shared_month',
            'cpi_month', 'cost_purchase_month', 'cost_online_earning_month', 'cost_market_month', 'profit_month'
        ])
        df_profit_month['profit_cumsum_month'] = df_profit_month['profit_month'].cumsum()

        # 返回数据格式化
        response = PredictResponse(
            code=HTTPStatus.OK,
            message="预测成功。",
            predict_response=SubPredictResponse(
                format_date=df_profit_day['format_date'].values.astype(str).tolist(),
                date_serial=df_profit_day['date_serial'].values.astype(np.int32).tolist(),
                new_install=df_profit_day['new_install'].values.astype(np.int32).tolist(),
                dau=df_profit_day['dau'].values.astype(np.int32).tolist(),
                arpu_in=np.round(df_profit_day['arpu_in'].values.astype(np.float32), 3).tolist(),
                arpu_ad=np.round(df_profit_day['arpu_ad'].values.astype(np.float32), 3).tolist(),
                official_income_aft_shared=df_profit_day['official_income_aft_share'].values.astype(np.int32).tolist(),
                local_income_aft_shared=df_profit_day['local_income_aft_share'].values.astype(np.int32).tolist(),
                income_in_aft_shared=df_profit_day['income_in_aft_share'].values.astype(np.int32).tolist(),
                income_ad=df_profit_day['income_ad'].values.astype(np.int32).tolist(),
                income_all=df_profit_day['income_all'].values.astype(np.int32).tolist(),
                income_all_cp_share=df_profit_day['income_all_cp_share'].values.astype(np.int32).tolist(),
                income_all_aft_shared=df_profit_day['income_all_aft_shared'].values.astype(np.int32).tolist(),
                cpi=np.round(df_profit_day['cpi'].values.astype(np.float32), 3).tolist(),
                cost_purchase=df_profit_day['cost_purchase'].values.astype(np.int32).tolist(),
                cost_online_earning=df_profit_day['cost_online_earning'].values.astype(np.int32).tolist(),
                cost_market=df_profit_day['cost_market'].values.astype(np.int32).tolist(),
                profit_daily=df_profit_day['profit_day'].values.astype(np.int32).tolist(),
                profit_cumsum=df_profit_day['profit_cumsum'].values.astype(np.int32).tolist(),
                format_month=df_profit_month['format_month'].values.astype(str).tolist(),
                new_install_month_avg=df_profit_month['new_install_month_avg'].values.astype(np.int32).tolist(),
                dau_month_avg=df_profit_month['dau_month_avg'].values.astype(np.int32).tolist(),
                arpu_in_month=np.round(df_profit_month['arpu_in_month'].values.astype(np.float32), 3).tolist(),
                arpu_ad_month=np.round(df_profit_month['arpu_ad_month'].values.astype(np.float32), 3).tolist(),
                official_income_aft_shared_month=df_profit_month['official_income_aft_shared_month'].values.astype(np.int32).tolist(),
                local_income_aft_shared_month=df_profit_month['local_income_aft_shared_month'].values.astype(np.int32).tolist(),
                income_in_aft_shared_month=df_profit_month['income_in_aft_shared_month'].values.astype(np.int32).tolist(),
                income_ad_month=df_profit_month['income_ad_month'].values.astype(np.int32).tolist(),
                income_all_month=df_profit_month['income_all_month'].values.astype(np.int32).tolist(),
                income_all_cp_share_month=df_profit_month['income_all_cp_share_month'].values.astype(np.int32).tolist(),
                income_all_aft_shared_month=df_profit_month['income_all_aft_shared_month'].values.astype(np.int32).tolist(),
                cpi_month=np.round(df_profit_month['cpi_month'].values.astype(np.float32), 3).tolist(),
                cost_purchase_month=df_profit_month['cost_purchase_month'].values.astype(np.int32).tolist(),
                cost_online_earning_month=df_profit_month['cost_online_earning_month'].values.astype(np.int32).tolist(),
                cost_market_month=df_profit_month['cost_market_month'].values.astype(np.int32).tolist(),
                profit_month=df_profit_month['profit_month'].values.astype(np.int32).tolist(),
                profit_cumsum_month=df_profit_month['profit_cumsum_month'].values.astype(np.int32).tolist(),
                re_rate_pre_360=re_rate_pre_360,
                lt_pre_360=lt_pre_360
            )
        )

        # TODO 日志记录
        current_app.logger.info(json.dumps({
            "config_ip": config_ip,
            "config_name": config_name,
            "config_time": config_time,
            "country": country,
            "game": game,
            "request": body.model_dump_json(),
            "response": response.model_dump_json()
        }, ensure_ascii=False))

        return response
