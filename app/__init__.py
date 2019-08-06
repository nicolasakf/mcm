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

from views import index
from views import request_mes_data, request_monitor_data, request_page
