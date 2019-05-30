#!/bin/python
from app import app
import socket


app.run(host='0.0.0.0', port=10019, debug=True, threaded=True)
