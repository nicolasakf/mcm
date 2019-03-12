from .. import app
from flask import jsonify


@app.route('/sendMESData', methods=['POST'])
def send_mes_data():
    return jsonify({}), 200
