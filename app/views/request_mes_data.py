# -*- coding: utf-8 -*-
from .. import app
import json
from flask import request
import datetime as dt
import app.db_lib as db


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    output = {}

    try:
        start_date_str = request.json['date-start']
        end_date_str = request.json['date-end']
    except KeyError:
        start_date_str = request.json['date']
        end_date_str = None

    machine_dict = {'1': 7654321, '2': 1234567}
    if end_date_str is None:
        mes = db.select_mes_daily(machine_dict[machine_id], start_date_str, host='localhost', user='romi',
                                  password='romiconnect')
    else:
        mes = db.select_mes_period(machine_dict[machine_id], start_date_str, end_date_str, host='localhost', user='romi',
                                   password='romiconnect')
    if mes.empty:
        output['msg'] = "Não existe relatório para a data selecionada."
    mes.to_excel('/Users/NicolasFonteyne/Downloads/{} {}.xlsx'.format(dt.date.today(), machine_dict[machine_id]),
                 index=False)

    # subprocess.Popen("open /Users/NicolasFonteyne/Downloads/{}.xlsx".format(dt.date.today()))
    # output['msg'] = "Exportado para /Users/NicolasFonteyne/Downloads/"

    output['ret_code'] = 0
    return json.dumps(output), 200
