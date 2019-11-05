"""
Modulo para copia da db na AWS no localhost
"""
from connection import insert
from queries import select

# machine_ids = [16019083464, 16019005452]
machine_ids = ['016-020207-456']
cols = ['absX', 'absY', 'absZ', 'alm_list_msg1', 'alm_list_msg2', 'alm_list_msg3', 'alm_stat', 'alm_type1',
           'alm_type2', 'alm_type3', 'auto_stat', 'cnc_type', 'counter', 'counter_tgt', 'edit_stat', 'emg_stat',
           'fdr', 'fdr_unit', 'ip', 'motion_stat', 'mt_type', 'prgname', 'rate', 'run_stat', 'series', 'spdl',
           'spdl_unit', 'timer_cut', 'timer_on', 'timer_op', 'pmc_alm1', 'pmc_alm2', 'pmc_alm3', 'pmc_alm4',
           'timer_run', 'name', 'date']
# while True:
# for mid in machine_ids:

for month in range(9, 11):
    for day in range(1,32):
        query = """
            select * from insper.MES
            where machine_id='{}' and month(date)={} and day(date)={}
            order by date desc
            limit 100
        """.format('016-020207-456', month, day)

        _data = select(query, host='3.217.217.48', user='romi', password='romiconnect')

        if not _data.empty:
            for i in range(len(_data)):
                values_str = "', '".join([str(_data.iloc[i][col]).replace("'", '"') for col in cols])
                columns_clause = ", ".join(cols) + ', machine_id'

                query = """
                    insert into insper.MES ({0})
                    values ('{1}', '{2}')
                """.format(columns_clause, values_str, '016-020207-456')
                insert(query, host='localhost', user='root', password='F1nt5yn6!')
