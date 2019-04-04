# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_compress import Compress
from app.core.monitor import Monitor

compress = Compress()

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

compress.init_app(app)

monitorDict = {'1': Monitor('1'), '2': Monitor('2')}

# cria pasta de upload se não existir
machine_list = ['1/', '2/']

for machine in machine_list:
    basedir = os.path.dirname(app.config['UPLOAD_FOLDER'] + machine)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

# Importar aqui a implementação dos WS
from views import index
from views import send_monitor_data, send_daq_data, send_feedrate_data, send_mes_data
from views import request_mes_data, request_monitor_data, request_page
from views import upload_program, list_program, download_program
