from .. import app
from flask import request, abort, render_template
from app.core.program import ProgramStorage


@app.route('/maquina/<machine_id>/uploadProgram', methods=['POST'])
def upload_program(machine_id):
    ps = ProgramStorage.Instance()

    if request.json is not None:
        file_list = request.json['file_list']
        if file_list is not None:
            for name in file_list:
                ps.add_program(machine_id, name)

                path = app.config['UPLOAD_FOLDER'] + machine_id + '/' + name
                open(path, 'a').close()
    else:
        abort(400)

    return "", 200
