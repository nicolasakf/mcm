# -*- coding: utf-8 -*-
"""
This route callback is called whenever MES data is requested
"""
from .. import app
import os
import json
from flask import request, send_file
import datetime as dt
import app.db_lib as db
import stats


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid

    mid = machine_id
    out = {}

    start_date_str = request.json['date-start']
    start = start_date_str
    end_date_str = request.json['date-end']
    end = end_date_str

    mes = db.select_mes_period(machine_dict[machine_id], start_date_str, end_date_str)

    if mes.empty:
        out['ret_code'] = 9
        out['msg'] = "Não há dados para o período selecionado"
    else:
        if not request.json['download']:
            df_dict = stats.timebar_enumerate(mes,
                                              ['alm_list_msg1', 'alm_list_msg2', 'alm_list_msg3', 'alm_stat',
                                               'alm_type1', 'alm_type2', 'alm_type3',
                                               'auto_stat', 'edit_stat', 'emg_stat', 'motion_stat', 'run_stat',
                                               'pmc_alm1', 'pmc_alm2', 'pmc_alm3',
                                               'pmc_alm4', 'prgname'])
            prep_auto = stats.prep_auto(df_dict)
            avail = stats.avail(mes)
            time_cut = stats.time_cut(mes)
            comp = stats.compound(df_dict)
            out.update(stats.export_figures(stats.plot_compound(prep_auto)))
            out.update(stats.export_figures(stats.plot_compound(avail), clear=False))
            out.update(stats.export_figures(
                stats.plot_compound(time_cut,
                                    value=prep_auto['Preparation Time / Automatic Time']['AUTO'],
                                    only_pct=True), clear=False
            ))
            out.update(stats.export_figures(stats.plot_compound(comp), clear=False))
            out.update(stats.export_figures(stats.plot_timeline(df_dict), clear=False))
            out['ret_code'] = 0
        else:
            out['ret_code'] = 1

    return json.dumps(out), 200


@app.route('/maquina/<machine_id>/downloads/')
def download_mes(machine_id='1'):
    from app.views.request_page import machine_dict
    global start, end, mid
    while (start is None) or (end is None) or (mid is None):
        pass
    mes = db.select_mes_period(machine_dict[machine_id], start, end)
    if not mes.empty:
        name = mes['name'][0]
        mes.drop('name', axis=1, inplace=True)
        for alm in ['pmc_alm1', 'pmc_alm2', 'pmc_alm3', 'pmc_alm4']:
            mes[alm] = mes[alm].str.split(' -', expand=True)[0]
    else:
        name = machine_dict[machine_id]

    filename = '{} {}.csv'.format(dt.datetime.now(), name)
    path = app.root_path + '/static/res/out/'
    mes.to_csv(path + filename, index=False)
    start = None;
    end = None;
    mid = None
    out = send_file(path + filename, as_attachment=True, attachment_filename=filename, cache_timeout=1)
    os.remove(path + filename)

    return out
