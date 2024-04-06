# -*- coding:utf-8 -*-
# @FileName  :  app.py
# @Time      :  2024/03/31 17:15:46
# @Author    :  Lotuslaw
# @Desc      :  app


import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))


from flask import Flask
import logging
from flask_cors import CORS
from utils.log_util import handler
from utils.exception_handler import handle_exception
from views.views_predict import PredictView
from views.views_re_predict import RePredictView


app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)
app.errorhandler(Exception)(handle_exception)


app.add_url_rule('/predict', view_func=PredictView.as_view('predict'))
app.add_url_rule('/repredict', view_func=RePredictView.as_view('repredict'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
