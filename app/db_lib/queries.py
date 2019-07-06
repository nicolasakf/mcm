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


def select_mes(machine_id, start, end, **kwargs):

    _query = """
        select * from insper.MES
        where MES.machine_id='{}'
        and date >= '{}' and date <= '{}'
    """.format(machine_id, start, end)
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
def new_user(name, pwd, company):

    _query = """
        select name from insper.user
        where name='{}'
    """.format(name)
    user_exists = not select(_query).empty
    if user_exists:
        raise ValueError('Ja existe um usuario com esse nome, favor escolher outro.')

    _query = """
        select company_id, name from insper.company
        where name='{}'
    """.format(company)
    _df = select(_query)
    try:  company = _df.iloc[0]['company_id']
    except IndexError:  raise IndexError('Nao foi possivel achar a companhia especificada: {}'.format(company))

    _query = """
        insert into `insper`.user (user_id, name, password, company_id)
        select if(max(user_id) is null, 1, max(user_id)+1), '{}', '{}', '{}' from insper.user
    """.format(name, pwd, company)
    insert(_query)

# new_user('nicolasakf', 'nicolas123', 'Insper')


def new_machine(serial, name, **kwargs):

    _query = """
        select machine_id from insper.machine
        where machine_id='{}'
    """.format(serial)
    mach_exists = not select(_query).empty
    if mach_exists:
        raise ValueError('Essa maquina ja esta listada na base de dados')

    _cols_str = ', '.join(['machine_id', 'name']+[k for k, v in kwargs if v is not None])
    _vals_str = ", ".join(["'{}'".format(serial), "'{}'".format(name)]+["'{}'".format(v) for k, v in kwargs if v is not None])

    _query = """
        insert into insper.machine ({cols})
        values({values})
    """.format(values=_vals_str, cols=_cols_str)
    insert(_query)

# new_machine('7654321', 'INSPER_ROMI')


def new_company(name, **kwargs):

    _query = """
        select name from insper.company
        where name='{}'
    """.format(name)
    comp_exists = not select(_query).empty
    if comp_exists:
        raise ValueError('Essa empresa ja esta listada na base de dados')

    _cols_str = ', '.join(['company_id', 'name']+[k for k, v in kwargs if v is not None])
    _vals_str = ", ".join(["'{}'".format(name)]+["'{}'".format(v) for k, v in kwargs if v is not None])

    _query = """
        insert into insper.company ({cols})
        select if(max(company_id) is null, 1, max(company_id)+1), {values} from insper.company
    """.format(values=_vals_str, cols=_cols_str)
    insert(_query)

# new_company('Insper')
