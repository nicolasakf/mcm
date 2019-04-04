from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

USER = 'romi'
PWD = 'romi'


@auth.verify_password
def verify_password(username, password):
    out = False
    if (username == USER) and (password == PWD):
        out = True

    return out


def auth_user(user, passwd):
    out = False
    if(user == USER) and (passwd == PWD):
        out = True

    return out