from .. import app, monitorDict
from flask import request, abort, jsonify
from app.core.utils import auth_user

@app.route('/sendFeedRateData', methods=['POST'])
def send_feed_rate_data():
    if not request.json:
        abort(400)

    user = request.json.get('user')
    passwd = request.json.get('passwd')
    if not auth_user(user, passwd):
        abort(400)

    machine_id = request.json.get('machineID');

    if machine_id is not None:
        monitor = monitorDict[str(machine_id)]

        monitor.set_vel(
            request.json.get('VelX'),
            request.json.get('VelY'),
            request.json.get('VelZ'),
            request.json.get('counter')
        )
        return jsonify({}), 200

    else:
        abort(400)
