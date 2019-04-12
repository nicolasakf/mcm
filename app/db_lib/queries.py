from connection import select, insert


# SELECT QUERIES -------------------------------------------------------------------------------------------------------

def select_monitor(user_id, machine_id, **kwargs):

    _query = """
        select * from romi_connect.monitor
        where monitor.user_id={}
            and monitor.machine_id={}
    """.format(user_id, machine_id)
    _df = select(_query, **kwargs)
    _df.drop(['user_id', 'machine_id'], axis=1, inplace=True)

    return _df.iloc[0, :]


# INSERT QUERIES -------------------------------------------------------------------------------------------------------

