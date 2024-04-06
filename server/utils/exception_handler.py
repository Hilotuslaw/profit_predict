# -*- coding: UTF-8 -*-
# @FileName  :  exception_handler.py
# @Time      :  2024/03/31 19:27:57
# @Author    :  Lotuslaw
# @Desc      :  


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


from models.req_resp_model import PredictResponse
from flask_pydantic import validate
from flask import current_app
from http import HTTPStatus
import traceback


@validate()
def handle_exception(error) -> PredictResponse:
    current_app.logger.error(traceback.format_exc())
    response = PredictResponse(code=HTTPStatus.BAD_REQUEST, message="预测失败")
    return response
