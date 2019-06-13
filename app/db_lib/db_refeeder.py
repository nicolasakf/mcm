"""
Modulo para copia da db na AWS no localhost
"""

from connection import insert
from queries import select_last_mes

machine_ids = [16019083464, 16019005452]
while True:

    for mid in machine_ids:
        _data = select_last_mes(mid)

        values_str = "', '".join([str(_data['date']), str(_data['spdl']), str(_data['emg_stat']),
                                  str(_data['alm_stat']), str(_data['absX']), str(_data['absY']),
                                  str(_data['absZ']), str(_data['timer_cut']), str(_data['timer_on']),
                                  str(_data['timer_op']), str(_data['timer_run']), str(mid), _data['pmc_alm1'],
                                  _data['pmc_alm2'], _data['pmc_alm3'], _data['pmc_alm4']])
        query = """
            insert into `romi_connect`.monitor (date, spdl, emg_stat, alm_stat, absX, absY, absZ,
                                                timer_cut, timer_on, timer_op, timer_run, machine_id, 
                                                pmc_alm1, pmc_alm2, pmc_alm3, pmc_alm4)
            values ('{values}')
            on duplicate key update date=values(date), spdl=values(spdl), emg_stat=values(emg_stat),
                                    alm_stat=values(alm_stat),
                                    absX=values(absX), absY=values(absY), absZ=values(absZ),
                                    timer_cut=values(timer_cut), timer_on=values(timer_on), timer_op=values(timer_op),
                                    timer_run=values(timer_run), pmc_alm1=values(pmc_alm1), pmc_alm2=values(pmc_alm2),
                                    pmc_alm3=values(pmc_alm3), pmc_alm4=values(pmc_alm4)
        """.format(values=values_str)
        insert(query, host='localhost', user='root', password='F1nt5yn6!')
