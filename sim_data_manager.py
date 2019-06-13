    #!/bin/python
# -*- coding: utf-8 -*-
from app.models.models import Machine, MachineStop, Report
from app import db
from datetime import date, timedelta, time, datetime, MINYEAR
from random import randint, choice, uniform
import sys

turn_start = [
    datetime(MINYEAR, 1, 1, hour=6),
    datetime(MINYEAR, 1, 1, hour=14),
    datetime(MINYEAR, 1, 1, hour=22)]

reason_list = [
    "Limpeza",
    "Troca inserto ferramenta",
    "Aguardando medicoes trid.",
    "Setup/Ajuste"
]


def main():
    if len(sys.argv) != 3:
        exit()

    clean_db()
    create_sim_data()


def clean_db():
    tables = [MachineStop, Report, Machine]

    for table in tables:
        table.query.delete()
        db.session.commit()


def create_sim_data():
    id_list = create_machines()

    for id in id_list:
        create_reports(id)


def create_machines():
    out = []

    machine = Machine(
        name= "Fanuc",
        pn= "M28405/406",
        scc="81822",
        celula="ROMI",
        cnc="Siemens SINUMERIK 840D sl/828D",
        cnc_sw_ver="Version 4.5 SP3",
        mon_hw_ver="O7S-NI-02.01.03",
        mon_sw_ver="O7S-SM-01.03.02",
        img_filename="romi_dcm620_5x.jpg",
        manual_filename="T94400B.pdf",
        serial="016019052420"
    )
    out.append(add_to_db(machine))

    machine = Machine(
        name="Romi",
        pn="M28405/406",
        scc="81822",
        celula="SCANIA",
        cnc="Siemens SINUMERIK 840D sl/828D",
        cnc_sw_ver="Version 4.5 SP3",
        mon_hw_ver="O7S-NI-02.01.03",
        mon_sw_ver="O7S-SM-01.03.02",
        img_filename="maq_romi_gl_350b.jpg",
        manual_filename="T96167B.pdf",
        serial="016019052499"
    )
    out.append(add_to_db(machine))

    return out


def create_reports(machine_id):
    before = int(sys.argv[1])
    after = int(sys.argv[2])
    start_date = date.today() - timedelta(days=before)
    delta = timedelta(days=(before + after))

    for i in range(delta.days):
        print("Criando relatório: " + str(start_date + timedelta(days=i)) + " (Maquina: " + str(machine_id) + ")")
        gen_report_data(machine_id, start_date + timedelta(days=i))


def gen_report_data(machine_id, date):

    pieces_t1 = randint(15, 20)
    pieces_t2 = randint(15, 20)
    pieces_t3 = randint(15, 20)

    # calculo de desempenho
    performance = uniform(0.8, 1.0)

    # qualidade variando entre 0,9 e 1,0
    quality = uniform(0.8, 1.0)

    # calculo de disponibilidade
    availability = uniform(0.8, 1.0)

    # calculo oee
    oee = availability * performance * quality

    report = Report(
        date=date,
        resp_name="Raphael",
        prod_amount_t1=pieces_t1,
        prod_amount_t2=pieces_t2,
        prod_amount_t3=pieces_t3,
        op_amount_t1=randint(0, 3),
        op_amount_t2=randint(0, 3),
        op_amount_t3=randint(0, 3),
        idx_avail=availability,
        idx_perf=performance,
        idx_quality=quality,
        idx_oee=oee,
        machine_id=machine_id
    )

    # grava no banco de dados
    report_id = add_to_db(report)

    # gera os dados de parada da maquina
    gen_stop_machine_data(report_id, date)


def gen_stop_machine_data(report_id, date):
    name_idx = 1
    index = 0
    total_stop_time = [0, 0, 0]

    for turn in range(3):
        is_stop = False
        start_time = turn_start[turn].replace(year=date.year, month=date.month, day=date.day)
        period_counter = 0

        while period_counter is not 480:
            if is_stop:
                duration = randint(10, 60)
            else:
                duration = randint(60, 480)

            period_counter += duration

            # ajusta duracao da ultima parada
            if period_counter > 480:
                duration -= period_counter - 480
                period_counter = 480

            end_time = start_time + timedelta(minutes=duration)
            if is_stop:
                stop_name = "P" + str(name_idx)
                reason = choice(reason_list)
            else:
                stop_name = ""
                reason = ""

            stop_entry = MachineStop(
                turn_num=turn+1,
                name=stop_name,
                dateStart=start_time.date(),
                timeStart=time(start_time.hour, start_time.minute, start_time.second),
                dateEnd=end_time.date(),
                timeEnd=time(end_time.hour, end_time.minute, end_time.second),
                reason= reason,
                report_id = report_id
            )

            db.session.add(stop_entry)

            # acumula o tempo de parada do turno
            if is_stop:
                total_stop_time[turn] += duration
                name_idx += 1

            index += 1
            start_time = end_time
            # alterna entre periodos de paradas e funcionamento
            is_stop = not is_stop

    db.session.flush()
    db.session.commit()

    return total_stop_time


def add_to_db(obj):

    db.session.add(obj)
    db.session.flush()
    db.session.refresh(obj)
    db.session.commit()

    return obj._id

if __name__ == "__main__":
    main()
