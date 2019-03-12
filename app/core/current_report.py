from datetime import datetime, date, time, timedelta


class CurrentReport:

    last_run_time = None
    total_run_time = None
    power_on_time = None
    date = None
    parts_count = None
    planned_time = None

    def __init__(self):
        self.total_run_time = 0
        self.last_run_time = 0
        self.power_on_time = 0
        self.date = datetime.combine(date.today(), time(6,0,0))
        self.parts_count = [0, 0, 0]
        self.planned_time = 0
        return

    def is_today_report(self):
        out = True
        if datetime.now() - self.date > timedelta(days=1):
            out = False

        return out

    def set_runtime(self, value):
        if value < self.last_run_time:
            self.total_run_time += self.last_run_time

        self.last_run_time = value

    def set_power_on(self, value):
        self.power_on_time = value

    def set_planned_time(self, value):
        self.planned_time = value

    def set_total_parts(self, value):
        turn_idx = self.get_turn_idx()

        if turn_idx == 0:
            self.parts_count[0] = value

        elif turn_idx == 1:
            self.parts_count[1] = value - self.parts_count[0]

        else:
            self.parts_count[2] = \
                value - self.parts_count[0] - self.parts_count[1]

    def get_turn_idx(self):
        delta = datetime.now() - self.date
        out = 0

        if timedelta(hours=8) <= delta < timedelta(hours=16):
            out = 1

        elif delta >= timedelta(hours=16):
            out = 2

        return out

    def get_availability(self):
        out = 0
        if self.planned_time > 0:
            out = float(self.total_run_time + self.last_run_time)/(self.planned_time)

        return out

    def get_parts_per_hour(self):
        total = 0
        for turn_count in self.parts_count:
            total += turn_count;

        out = 0
        if self.planned_time != 0:
            out = float(total*3600)/(self.planned_time)

        return out

    def save_report(self):
        return True

    def __repr__(self):
        out = "CurrentReport(last_run_time:{0}, total_run_time:{1}, power_on_time:{2}, date:{3}, parts_count:{4}, planned_time:{5}, avail:{6})\n"\
            .format(self.last_run_time,
                         self.total_run_time,
                         self.power_on_time,
                         self.date,
                         self.parts_count,
                         self.planned_time,
                         self.get_availability())

        return out


