from time import sleep
import datetime as dt

import numpy as np

from connection import insert


time = 0
while True:
    rpm = np.random.randint(0, 15)
    power = np.random.randint(0, 100)
    status = np.random.randint(0, 3)
    run_time = dt.timedelta(seconds=time)
    power_on = dt.timedelta(seconds=time)
    operating_time = dt.timedelta(seconds=time)
    availability = .5 + np.random.rand()/10
    rate = .5 + np.random.rand()/10

    values_str = "', '".join([str(rpm), str(power), str(status),
                              # str(run_time), str(power_on), str(operating_time),
                              str(availability), str(rate), '0', '0'])
    query = """
        insert into `romi_connect`.monitor (rpm, power, status,
                                            # run_time, power_on, operating_time,
                                            availability, rate, user_id, machine_id)
        values ('{values}')
        on duplicate key update rpm=values(rpm), power=values(power), status=values(status),
                                # run_time, power_on, operating_time,
                                availability=values(availability), rate=values(rate)
    """.format(values=values_str)
    insert(query)
    sleep(1)
    time += 1
