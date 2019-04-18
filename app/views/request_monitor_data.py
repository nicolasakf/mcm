import datetime as dt

from .. import app, monitorDict
import json
from app import db_lib as db


@app.route('/maquina/<machine_id>/requestMonitorData', methods=['POST'])
def request_monitor_data(machine_id='1'):

    _data = db.select_monitor(user_id=0, machine_id=0)
    dt_init = dt.datetime(2000, 1, 1)

    monitor = monitorDict[machine_id]

    return json.dumps({
        "posx": "{:10.3f}".format(monitor.posX),
        "posy": "{:10.3f}".format(monitor.posY),
        "posz": "{:10.3f}".format(monitor.posZ),
        "spindle_load": _data['power'],
        "spindle_speed": _data['rpm'],
        "cutting_time": str(monitor.cuttingTime),
        "operating_time": (dt_init + dt.timedelta(seconds=_data['operating_time'])).strftime('%H:%M:%S'),
        "poweron_time": (dt_init + dt.timedelta(seconds=_data['power_on'])).strftime('%H:%M:%S'),
        "run_time": (dt_init + dt.timedelta(seconds=_data['run_time'])).strftime('%H:%M:%S'),
        "parts_required": "{:10.0f}".format(monitor.reqParts),
        "parts_count": "{:10.0f}".format(monitor.totalParts),
        "velx": monitor.velX,
        "vely": monitor.velY,
        "velz": monitor.velZ,
        "alarm_number": monitor.lastAlarm,
        "alarm_high": monitor.actualAlarm,
        "avail": _data['availability'],
        "feedrate": _data['status'],
        "parts_hour": "{:6.2f}".format(monitor.currentReport.get_parts_per_hour())
    })