#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")";pwd)

cd ${pwd_dir}/../

source ~/venv_profit_predict/bin/activate

supervisorctl -c ./config/supervisord.conf shutdown