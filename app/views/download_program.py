from .. import app
from flask import request, send_from_directory
import os.path


@app.route('/maquina/<machine_id>/downloadProgram', methods=['POST'])
def download_program(machine_id):
    if request.json is not None:
        file_name = request.json['name']

        path = app.config['UPLOAD_FOLDER'] + machine_id + '/' + file_name
        if os.path.isfile(path):
            return send_from_directory(app.config['UPLOAD_FOLDER'] + machine_id + '/', file_name)

    return "", 404