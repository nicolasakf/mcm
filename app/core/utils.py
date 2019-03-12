from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    out = False
    if (username == "omega7romi") and (password == 'expomafe2017'):
        out = True

    return out


def auth_user(user, passwd):
    out = False
    if(user == "omega7romi") and (passwd == 'expomafe2017'):
        out = True

    return out