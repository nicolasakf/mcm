import datetime as dt

from .. import app, monitorDict
import json
from app import db_lib as db


@app.route('/maquina/<machine_id>/requestMonitorData', methods=['POST'])
def request_monitor_data(machine_id='1'):
    machine_dict = {'1': 7654321, '2': 1234567}

    _data = db.select_last_mes(machine_id=machine_dict[machine_id], host='localhost', user='romi',
                               password='romiconnect')

    # status treatment
    _data['status'] = 1
    if _data['emg_stat'] != 'Not emergency':  _data['status'] = 4
    elif _data['alm_stat'] != '****':  _data['status'] = 3
    elif _data['pmc_alm1'] != '-1 - NO ALARM': _data['status'] = 3
    elif _data['pmc_alm2'] != '-1 - NO ALARM': _data['status'] = 3
    elif _data['pmc_alm3'] != '-1 - NO ALARM': _data['status'] = 3
    # elif _data['pmc_alm4'] != '-1 - NO ALARM': _data['status'] = 3
    # elif _data['run_stat'] != '****':  _data['status'] = 1
    _data['timer_cut'] = dt.timedelta(_data['timer_cut'] / 60 / 60 / 24)
    _data['timer_op'] = dt.timedelta(_data['timer_op'] / 60 / 60 / 24)
    _data['timer_on'] = dt.timedelta(_data['timer_on'] / 60 / 60 / 24)
    _data['timer_run'] = dt.timedelta(_data['timer_run'] / 60 / 60 / 24)

    monitor = monitorDict[machine_id]

    _json = json.dumps({
        "posx": "{:10.3f}".format(_data['absX']),
        "posy": "{:10.3f}".format(_data['absY']),
        "posz": "{:10.3f}".format(_data['absZ']),
        "spindle_load": 0,
        "spindle_speed": _data['spdl'],
        "cutting_time": dhms(_data['timer_cut']),
        "operating_time": dhms(_data['timer_op']),
        "poweron_time": dhms(_data['timer_on']),
        "run_time": dhms(_data['timer_run']),
        "parts_required": "{:10.0f}".format(monitor.reqParts),
        "parts_count": "{:10.0f}".format(monitor.totalParts),
        "velx": monitor.velX,
        "vely": monitor.velY,
        "velz": monitor.velZ,
        "alarm_number": monitor.lastAlarm,
        "alarm_high": monitor.actualAlarm,
        # "avail": _data['availability'],
        "avail": 0,
        "feedrate": _data['status'],
        # "status": _data['status'],
        "parts_hour": "{:6.2f}".format(monitor.currentReport.get_parts_per_hour())
    })
    return _json


def dhms(td):
    return '{} dias {}:{}:{}'.format(td.days, td.seconds // 3600, (td.seconds // 60) % 60, td.seconds % 60)
