from .. import app, monitorDict
from flask import request, abort, jsonify
from app.core.utils import auth_user


@app.route('/sendMonitorData', methods=['POST'])
def send_monitor_data():
    if not request.json:
        return "Not a JSON!\n", 400

    user = request.json.get('user')
    passwd = request.json.get('passwd')
    if not auth_user(user, passwd):
        return "Auth fail!\n", 400

    machine_id = request.json.get('machineID');

    if machine_id is None:
        return "Machine not found!\n", 400

    monitor = monitorDict[str(machine_id)]

    monitor.check_report_date()

    monitor.currentReport.set_runtime(request.json.get('RunTime'))
    monitor.currentReport.set_planned_time(request.json.get('PowerOn')*60)
    monitor.currentReport.set_power_on(request.json.get('PowerOn'))
    monitor.currentReport.set_total_parts(request.json.get('TotalParts'))

    monitor.set_pos(
        request.json.get('PosX'),
        request.json.get('PosY'),
        request.json.get('PosZ')
    )

    monitor.set_spindle_gauges(
        request.json.get('SpindleLoad'),
        request.json.get('SpindleSpeed')
    )

    monitor.set_alarm(
        request.json.get('LastAlarm'),
        request.json.get('ActualAlarm'),
        request.json.get('AlarmTime')
    )

    monitor.set_feedrate_nck(
        request.json.get('FeedRateNck')
    )

    monitor.set_parts(
        request.json.get('ReqParts'),
        request.json.get('TotalParts')
    )

    monitor.set_times(
        request.json.get('Operating'),
        request.json.get('PowerOn'),
        request.json.get('CuttingTime'),
        request.json.get('RunTime')
    )

    return "", 200

