import mysql.connector

HOST = 'localhost'
USER = 'root'
PWD = 'F1nt5yn6!'
DB = 'romi_connect'


def _init_connection(host=HOST, user=USER, password=PWD, db=DB):

    _conn = mysql.connector.connect(
        use_pure=False,
        host=host,
        user=user,
        password=password,
        database=db
    )
    _cursor = _conn.cursor()

    return _conn, _cursor


def insert(query, values=None, **kwargs):

    _conn, _cursor = _init_connection(**kwargs)
    if values is None:  _cursor.execute(query)
    else:  _cursor.executemany(query, values)
    _conn.commit()
    _conn.close()
