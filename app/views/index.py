from .. import app
from flask import render_template
from app.core.utils import auth
from sim_data_manager import create_machines, clean_db


@app.route('/')
@auth.login_required
def dashboard():
    """ Root route """
    from app.core.utils import USER_ID
    clean_db()
    create_machines(USER_ID)
    return render_template('dashboard.html')


@app.route('/maquina/<machine_id>')
@app.route('/maquina/<machine_id>/')
@auth.login_required
def index_handler(machine_id='1'):
    """ Renders layout.html page accordingly to selected machine in dashboard """
    return render_template('layout.html',
                           machine_id=machine_id)
