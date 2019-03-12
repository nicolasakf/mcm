from .. import app, monitorDict
import json


@app.route('/maquina/<machine_id>/requestMonitorData', methods=['POST'])
def request_monitor_data(machine_id='1'):
    monitor = monitorDict[machine_id]

    return json.dumps({
        "posx": "{:10.3f}".format(monitor.posX),
        "posy": "{:10.3f}".format(monitor.posY),
        "posz" : "{:10.3f}".format(monitor.posZ),
        "spindle_load": monitor.spindleLoad,
        "spindle_speed": monitor.spindleSpeed,
        "cutting_time": str(monitor.cuttingTime),
        "operating_time": str(monitor.operatingTime),
        "poweron_time": str(monitor.powerOnTime),
        "run_time": str(monitor.runTime),
        "parts_required": "{:10.0f}".format(monitor.reqParts),
        "parts_count": "{:10.0f}".format(monitor.totalParts),
        "velx": monitor.velX,
        "vely": monitor.velY,
        "velz": monitor.velZ,
        "alarm_number": monitor.lastAlarm,
        "alarm_high": monitor.actualAlarm,
        "avail": monitor.currentReport.get_availability(),
        "feedrate": monitor.feedRateNck,
        "parts_hour": "{:6.2f}".format(monitor.currentReport.get_parts_per_hour())
    })