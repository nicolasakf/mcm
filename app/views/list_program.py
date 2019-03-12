from .. import app
from flask import request, abort, render_template
from app.core.program import ProgramStorage


@app.route('/maquina/<machine_id>/listProgram', methods=['POST'])
def list_program(machine_id):
    ps = ProgramStorage.Instance()

    return render_template("file_explorer.html",
                           name_list=ps.get_program_list(machine_id))
