# -*- coding: utf-8 -*-
"""
This route callback is called whenever MES data is requested (either daily or period tabs)
"""
from .. import app
import os
import json
from flask import request, send_file
import datetime as dt
import app.db_lib as db


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    from app.views.request_page import machine_dict
    output = {}

    try:
        start_date_str = request.json['date-start']
        end_date_str = request.json['date-end']
    except KeyError:
        start_date_str = request.json['date']
        end_date_str = None

    if end_date_str is None:
        mes = db.select_mes_daily(machine_dict[machine_id], start_date_str, host='localhost', user='romi',
                                  password='romiconnect')
    else:
        mes = db.select_mes_period(machine_dict[machine_id], start_date_str, end_date_str, host='localhost', user='romi',
                                   password='romiconnect')
    if mes.empty:
        output['msg'] = "Não existe relatório para a data selecionada."

    filename = '{} {}.xlsx'.format(dt.date.today(), machine_dict[machine_id])
    path = app.root_path + '/static/res/out'
    mes.to_excel(path + filename, index=False)
    return send_file(path + filename)

    # subprocess.Popen("open /Users/NicolasFonteyne/Downloads/{}.xlsx".format(dt.date.today()))
    # output['msg'] = "Exportado para /Users/NicolasFonteyne/Downloads/"

    # output['ret_code'] = 0
    return json.dumps(output), 200