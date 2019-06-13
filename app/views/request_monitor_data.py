import datetime as dt

from .. import app, monitorDict
import json
from app import db_lib as db


@app.route('/maquina/<machine_id>/requestMonitorData', methods=['POST'])
def request_monitor_data(machine_id='1'):
    machine_dict = {'1': 16019005452, '2': 16019083464}

    _data = db.select_monitor(machine_id=machine_dict[machine_id], host='localhost', user='root', password='F1nt5yn6!')

    # status treatment
    _data['status'] = 1
    if _data['emg_stat'] != 'Not emergency':  _data['status'] = 4
    elif _data['alm_stat'] != '****':  _data['status'] = 3
    elif _data['pmc_alm1'] != '-1 - NO ALARM': _data['status'] = 3
    elif _data['pmc_alm2'] != '-1 - NO ALARM': _data['status'] = 3
    elif _data['pmc_alm3'] != '-1 - NO ALARM': _data['status'] = 3
    # elif _data['pmc_alm4'] != '-1 - NO ALARM': _data['status'] = 3
    # elif _data['run_stat'] != '****':  _data['status'] = 1
    dt_init = dt.datetime(2000, 1, 1)

    monitor = monitorDict[machine_id]

    _json = json.dumps({
        "posx": "{:10.3f}".format(_data['absX']),
        "posy": "{:10.3f}".format(_data['absY']),
        "posz": "{:10.3f}".format(_data['absZ']),
        "spindle_load": 0,
        "spindle_speed": _data['spdl'],
        "cutting_time": (dt_init + dt.timedelta(seconds=_data['timer_cut'])).strftime('%H:%M:%S'),
        "operating_time": (dt_init + dt.timedelta(seconds=_data['timer_op'])).strftime('%H:%M:%S'),
        "poweron_time": (dt_init + dt.timedelta(seconds=_data['timer_on'])).strftime('%H:%M:%S'),
        "run_time": (dt_init + dt.timedelta(seconds=_data['timer_run'])).strftime('%H:%M:%S'),
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
