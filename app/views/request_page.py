"""
This route callback is called whenever a different machine is selected in the dashboard
"""
from flask import request
import datetime as dt
from .. import app
from flask import render_template
from app.models.models import Machine
from app.core.monitor import Monitor


pageDict = {
    'monitor': 'monitor.html',
    'home': 'home.html',
    'program': 'program.html',
    'support': 'support.html',
    'camera': 'camera.html',
    'mes_daily': 'mes_daily.html',
    'mes_period': 'mes_period.html',
    'manual': 'manual.html',
    'corte': 'corte.html',
    'medicao': 'medicao.html',
    'folha': 'folha.html',
    'dashboard': 'dashboard.html'
}

machine_list = None
monitor_dict = None
machine_dict = None


@app.route('/maquina/<machine_id>/requestPage', methods=['POST'])
def request_page_handler(machine_id='1'):
    data = request.get_json()
    html = ''
    http_code = 200

    _machine_list = Machine.query.all()
    machine = _machine_list[(int(machine_id) - 1)]

    _machine_list = Machine.query.all()
    global machine_list, monitor_dict, machine_dict
    machine_list = ['{}/'.format(i+1) for i in range(len(_machine_list))]
    monitor_dict = {'{}'.format(i+1): Monitor(str(i+1)) for i in range(len(_machine_list))}
    machine_dict = {'{}'.format(i+1): m.serial for i, m in enumerate(_machine_list)}

    if machine is not None:
        machine_data = {
            "name": machine.name,
            "img": machine.img_filename,
            "cnc": machine.cnc,
            "cnc_swv": machine.cnc_sw_ver,
            "mon_hw_ver": machine.mon_hw_ver,
            "mon_sw_ver": machine.mon_sw_ver,
            "manual": machine.manual_filename,
            "serial": machine.serial,
            "id": machine_id
        }

    if data is not None:
        page_url = pageDict[data['page-id']]
        html = render_template(page_url,
                               machine=machine_data,
                               cam_addr=app.config['CAM_STREAM'][machine_id])
    else:
        http_code = 400

    return html, http_code
