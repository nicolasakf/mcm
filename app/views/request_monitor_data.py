# -*- coding: utf-8 -*-
"""
This route callback is recursively called (1s interval) whenever a monitor tab is accessed
"""
import datetime as dt

from .. import app
import json
from app import db_lib as db


@app.route('/maquina/<machine_id>/requestMonitorData', methods=['POST'])
def request_monitor_data(machine_id='1'):
    from app.views.request_page import monitor_dict, machine_dict

    data = db.select_mes_realtime(machine_id=machine_dict[machine_id])

    # status treatment
    data['status'] = 1
    if data['emg_stat'] != 'Not emergency':  data['status'] = 4
    elif data['alm_stat'] != '****':  data['status'] = 3
    elif data['pmc_alm1'] != '-1 - NO ALARM': data['status'] = 3
    elif data['pmc_alm2'] != '-1 - NO ALARM': data['status'] = 3
    elif data['pmc_alm3'] != '-1 - NO ALARM': data['status'] = 3
    elif data['pmc_alm4'] != '-1 - NO ALARM': data['status'] = 3
    # elif data['run_stat'] != '****':  data['status'] = 1
    data['timer_cut'] = dt.timedelta(data['timer_cut'] / 60 / 60 / 24)
    data['timer_op'] = dt.timedelta(data['timer_op'] / 60 / 60 / 24)
    data['timer_on'] = dt.timedelta(data['timer_on'] / 60 / 60 / 24)
    data['timer_run'] = dt.timedelta(data['timer_run'] / 60 / 60 / 24)

    monitor = monitor_dict[machine_id]

    _json = json.dumps({
        "posx": "{:10.3f}".format(data['absX']),
        "posy": "{:10.3f}".format(data['absY']),
        "posz": "{:10.3f}".format(data['absZ']),
        # "spindle_load": 0,
        "spindle_load": data['rate'],
        # "spindle_speed": data['spdl'],
        "cutting_time": dhm(data['timer_cut']),
        "operating_time": dhm(data['timer_op']),
        "poweron_time": dhm(data['timer_on']),
        "run_time": dhm(data['timer_run']),
        "parts_required": "{:10.0f}".format(monitor.reqParts),
        "parts_count": "{:10.0f}".format(monitor.totalParts),
        "velx": monitor.velX,
        "vely": monitor.velY,
        "velz": monitor.velZ,
        "alarm_number": monitor.lastAlarm,
        "alarm_high": monitor.actualAlarm,
        "avail": 0,
        "feedrate": data['status'],
        "spindle_speed": data['date'].strftime('%d-%m-%Y %H:%M:%S'),
        "parts_hour": "{:6.2f}".format(monitor.currentReport.get_parts_per_hour())
    })
    return _json


def dhm(td):
    return '{} d {:02d}:{:02d}'.format(td.days, td.seconds // 3600, (td.seconds // 60) % 60)
