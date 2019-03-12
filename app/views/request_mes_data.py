# -*- coding: utf-8 -*-
from .. import app
import json
from app.models.models import Report, Machine, MachineStop
from flask import request, abort
from datetime import datetime


@app.route('/maquina/<machine_id>/requestMESData', methods=['POST'])
def request_mes_data(machine_id='1'):
    output = {}

    if not request.json:
        abort(400)

    mes_type = request.json['type']
    if mes_type is None:
        abort(400)

    if mes_type == 'daily':
        start_date_str = request.json['date']
        if start_date_str is None:
            abort(400)

        report_list = Report.query.filter(
            Report.date == start_date_str,
            Report.machine_id == machine_id
        ).all()

    elif mes_type == 'period':
        start_date_str = request.json['date-start']
        end_date_str = request.json['date-end']

        if start_date_str is None or end_date_str is None:
            abort(400)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if (end_date - start_date).days < 0:
            output['ret_code'] = 1
            output['msg'] = "A data inicial deve ser a mesma ou anterior a data final."
            return json.dumps(output), 200

        report_list = Report.query.filter(
            Report.date.between(start_date_str, end_date_str),
            Report.machine_id == machine_id
        ).all()

    else:
        abort(400)

    if report_list is None or len(report_list) <= 0:
        output['ret_code'] = 2
        output['msg'] = "Não existe relatório para data selecionada."
        return json.dumps(output), 200

    machine = Machine.query.filter(Machine._id == machine_id).first()
    if machine is None:
        output['ret_code'] = 3
        output['msg'] = "Máquina não existe."
        return json.dumps(output), 200

    if mes_type == 'daily':
        data = {
            'scc': machine.scc,
            'celula': machine.celula,
            'resp': report_list[0].resp_name,
            'date-start': start_date_str,
            'pn': machine.pn
        }
    else:
        data = {
            'scc': machine.scc,
            'celula': machine.celula,
            'resp': report_list[0].resp_name,
            'date_start': start_date_str,
            'date_end': end_date_str,
            'pn': machine.pn
        }

    idx_avail = 0
    idx_perf = 0
    idx_quality = 0
    idx_oee = 0

    prod_amount_t1 = 0
    prod_amount_t2 = 0
    prod_amount_t3 = 0
    prod_amount_total = 0

    op_amount_t1 = 0
    op_amount_t2 = 0
    op_amount_t3 = 0

    prod_time_total = [[0, 0], [0, 0], [0, 0]]
    prod_time = [[], [], []]

    # acumula os dados dos relatorios
    for report in report_list:
        idx_avail += report.idx_avail
        idx_perf += report.idx_perf
        idx_quality += report.idx_quality
        idx_oee += report.idx_oee

        prod_amount_t1 += report.prod_amount_t1
        prod_amount_t2 += report.prod_amount_t2
        prod_amount_t3 += report.prod_amount_t3
        prod_amount_total += report.prod_amount_t1 + report.prod_amount_t2 + report.prod_amount_t3

        op_amount_t1 += report.op_amount_t1
        op_amount_t2 += report.op_amount_t2
        op_amount_t3 += report.op_amount_t3

        for turn in range(1, 4):
            time_running = 0
            time_stopped = 0
            stop_list = report.stops.filter(MachineStop.turn_num == turn).all()
            turn_data = []

            for stop in stop_list:
                start_day = 0
                end_day = 0

                if stop.dateStart.day > report.date.day:
                    start_day = 1

                if stop.dateEnd.day > report.date.day:
                    end_day = 1

                # valor só é guardado caso seja tipo diario
                if mes_type == 'daily':
                    stop_data = {
                        'id': stop.name,
                        'start': {
                            'd': start_day,
                            'h': stop.timeStart.hour,
                            'm': stop.timeStart.minute
                        },
                        'end': {
                            'd': end_day,
                            'h': stop.timeEnd.hour,
                            'm': stop.timeEnd.minute
                        },
                        'reason': stop.reason
                    }
                    turn_data.append(stop_data)

                # calcula tempos totais por turno
                dtime_start = datetime.combine(stop.dateStart, stop.timeStart)
                dtime_end = datetime.combine(stop.dateEnd, stop.timeEnd)
                delta = dtime_end - dtime_start

                # se nome da para é vazio, significa que é um periodo de execução
                if stop.name == "":
                    time_running += delta.seconds
                # senão é um periodo de parada
                else:
                    time_stopped += delta.seconds

            # valor só é guardado caso seja tipo diario
            if mes_type == 'daily':
                # teoricamente deve ser apenas 1 dia
                prod_time[turn-1] = turn_data

            # acumula os valores de todos os turnos
            prod_time_total[turn-1][0] += time_running
            prod_time_total[turn-1][1] += time_stopped

    # calcula as médias e cria a estrutura JSON
    report_amount = len(report_list)

    index = {
        'avail': idx_avail/report_amount,
        'perf': idx_perf/report_amount,
        'quality': idx_quality/report_amount,
        'oee': idx_oee/report_amount
    }

    prod_amount = {
        'turn1': float(prod_amount_t1)/report_amount,
        'turn2': float(prod_amount_t2)/report_amount,
        'turn3': float(prod_amount_t3)/report_amount,
        'total': float(prod_amount_total)/report_amount
    }

    op_amount = {
        'turn1': float(op_amount_t1)/report_amount,
        'turn2': float(op_amount_t2)/report_amount,
        'turn3': float(op_amount_t3)/report_amount
    }

    output['data'] = data
    output['index'] = index
    output['prodAmount'] = prod_amount
    output['opAmount'] = op_amount
    output['prodTimeTotal'] = prod_time_total

    # valor só é enviado caso seja tipo diario
    if mes_type == 'daily':
        output['prodTime'] = prod_time

    output['ret_code'] = 0

    return json.dumps(output), 200

