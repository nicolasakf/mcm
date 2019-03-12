from .. import app
from flask import jsonify


@app.route('/sendDAQData', methods=['POST'])
def send_daq_data():
    return jsonify({}), 200
