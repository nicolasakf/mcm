from connection import select, insert
from time import time


# SELECT QUERIES -------------------------------------------------------------------------------------------------------


def select_monitor(machine_id, **kwargs):

    _query = """
        select * from romi_connect.monitor
        where monitor.machine_id='{}'
    """.format(machine_id)
    _df = select(_query, **kwargs)
    _df.drop(['machine_id'], axis=1, inplace=True)

    return _df.iloc[0, :]


def select_mes(machine_id, **kwargs):

    _query = """
        select * from insper.MES
        where MES.machine_id='{}'
    """.format(machine_id)
    _df = select(_query, **kwargs)
    _df.drop(['machine_id'], axis=1, inplace=True)

    return _df


def select_last_mes(machine_id, profile=False, **kwargs):
    t = time()
    _query = """
        select * from insper.MES
        where MES.machine_id='{}'
        order by MES.date DESC
        limit 1;
    """.format(machine_id)
    _df = select(_query, **kwargs)
    _df.drop(['machine_id'], axis=1, inplace=True)
    if profile:  print 'Time to load data: {:.2f}'.format(time()-t)

    return _df.iloc[0, :]


# INSERT QUERIES -------------------------------------------------------------------------------------------------------
def new_user(name, psswd, company):

    if not isinstance(company, int):
        _query = """
            select company_id, name from romi_connect.company
            where name='{}'
        """.format(company)
        _df = select(_query)
        company = _df.iloc[0]['company_id']

    _query = """
        insert into `romi_connect`.user (user_id, name, password, company_id)
        select if(max(user_id) is null, 1, max(user_id)+1), '{}', '{}', '{}' from romi_connect.user
    """.format(name, psswd, company)
    insert(_query)


def new_machine(serial, name, **kwargs):

    _cols_str = ', '.join(['machine_id', 'name']+[k for k, v in kwargs if v is not None])
    _vals_str = ", ".join(["'{}'".format(serial), "'{}'".format(name)]+["'{}'".format(v) for k, v in kwargs if v is not None])

    _query = """
        insert into `romi_connect`.machine ({cols})
        values({values})
    """.format(values=_vals_str, cols=_cols_str)
    insert(_query)


def new_company(name, **kwargs):

    _cols_str = ', '.join(['company_id', 'name']+[k for k, v in kwargs if v is not None])
    _vals_str = ", ".join(["'{}'".format(name)]+["'{}'".format(v) for k, v in kwargs if v is not None])

    _query = """
        insert into `romi_connect`.company ({cols})
        select if(max(company_id) is null, 1, max(company_id)+1), {values} from `romi_connect`.company
    """.format(values=_vals_str, cols=_cols_str)
    insert(_query)

# new_machine(16019083464, 'ROMI GL 240M (TORRE M) A2-5 CURTO V3.0 FANUC 0I-TD - ENSINO')
# def assign_machine(username, machine_id):
#     pass

