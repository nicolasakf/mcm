#!/bin/python
from app import app

app.run(host='0.0.0.0', port=10002, debug=True, threaded=True)
