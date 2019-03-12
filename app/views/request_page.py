from flask import request
from .. import app
from flask import render_template, abort
from app.models.models import Machine

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


@app.route('/maquina/<machine_id>/requestPage', methods=['POST'])
def request_page_handler(machine_id='1'):
    data = request.get_json()
    html = ''
    http_code = 200

    machine_list = Machine.query.all()
    machine = machine_list[(int(machine_id) -1)]

    if machine is not None:
        machine_data = {
            "name": machine.name,
            "img": machine.img_filename,
            "cnc": machine.cnc,
            "cnc_swv": machine.cnc_sw_ver,
            "mon_hw_ver": machine.mon_hw_ver,
            "mon_sw_ver": machine.mon_sw_ver,
            "manual":machine.manual_filename,
            "serial":machine.serial
        }

    if data is not None:
        page_url = pageDict[data['page-id']]
        html = render_template(page_url,
                               machine=machine_data,
                               cam_addr=app.config['CAM_STREAM'][machine_id])
    else:
        http_code = 400

    return html, http_code
