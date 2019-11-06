from flask_httpauth import HTTPBasicAuth
from app import db_lib as db

auth = HTTPBasicAuth()
USER_ID = None


@auth.verify_password
def verify_password(username, password):
    user_list = db.get_user_list()
    try:
        pwd = user_list[username]
        if pwd != password:
            return False
        else:
            global USER_ID
            USER_ID = db.get_user_id(username)
            return True
    except KeyError:
        return False


def dhm(td):
    return '{} d {:02d}:{:02d}'.format(td.days, td.seconds // 3600, (td.seconds // 60) % 60)


def hms(td):
    return '{:02d}:{:02d}:{:02d}'.format(td.seconds // 3600, (td.seconds // 60) % 60, td.seconds % 60)


def h(td):
    return '{}h'.format(td.seconds // 3600)
