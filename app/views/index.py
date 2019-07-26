from .. import app
from flask import render_template
from app.core.utils import auth
from sim_data_manager import main


@app.route('/')
@auth.login_required
def dashboard():
    main()
    return render_template('dashboard.html')


@app.route('/maquina/<machine_id>')
@app.route('/maquina/<machine_id>/')
@auth.login_required
def index_handler(machine_id='1'):
    has_camera = True
    # if machine_id != '1' and machine_id != '2':
    #     abort(404)

    if machine_id == '2':
        has_camera = False

    return render_template('layout.html',
                           machine_id=machine_id,
                           has_camera=has_camera)
