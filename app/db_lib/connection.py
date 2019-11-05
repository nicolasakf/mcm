import mysql.connector
import pandas as pd

# HOST = '3.217.217.48'
# USER = 'romi'
# PWD = 'romiconnect'
HOST = 'localhost'
USER = 'root'
PWD = 'F1nt5yn6!'


def _init_connection(host=HOST, user=USER, password=PWD):
    """
    Creates a connection and a cursor to interact with the database
    :param host: str;
    :param user: str
    :param password: str;
    :return: connector, cursor
    """
    conn = mysql.connector.connect(
        use_pure=False,
        host=host,
        user=user,
        password=password,
    )
    cursor = conn.cursor()

    return conn, cursor


def select(query, **kwargs):
    """
    Generic select-type query executor
    :param query: str;
    :param kwargs: _init_connection keyword args
    :return: pd.DataFrame; query result
    """
    _conn, _ = _init_connection(**kwargs)
    _df = pd.read_sql(query, con=_conn)
    _conn.close()

    return _df


def insert(query, values=None, **kwargs):
    """
    Generic insert-type query executor
    :param query: str;
    :param values: list of values to be inserted. See MySQL docs for additional formatting instructions.
    :param kwargs: _init_connection keyword args
    :return: void;
    """
    _conn, _cursor = _init_connection(**kwargs)
    if values is None:  _cursor.execute(query)
    else:  _cursor.executemany(query, values)
    _conn.commit()
    _conn.close()
