from datetime import timedelta, datetime
from current_report import CurrentReport


class Monitor:
    def __init__(self, id):
        self.machine_id = id
        self.currentReport = CurrentReport()

    def set_pos(self, x, y, z):
        if x is not None:
            self.posX = x

        if y is not None:
            self.posY = y

        if z is not None:
            self.posZ = z

    def set_spindle_gauges(self, load, speed):
        if load is not None:
            if load < 0:
                self.spindleLoad = 0
            elif load > 100:
                self.spindleLoad = 100
            else:
                self.spindleLoad = load

        if speed is not None:
            if speed < 0:
                self.spindleSpeed = 0
            elif speed > 15000:
                self.spindleSpeed = 15
            else:
                self.spindleSpeed = speed/1000.0

    def set_parts(self, req, total):
        if req is not None:
            self.reqParts = req

        if total is not None:
            self.totalParts = total

    def set_alarm(self, last, actual, time):
        if last is not None:
            self.lastAlarm = last

        if actual is not None:
            self.actualAlarm = actual

        if time is not None:
            self.alarmTime = datetime.fromtimestamp(time)

    def set_times(self, op, pwr, cut, run):
        if op is not None:
            self.operatingTime = timedelta(seconds=long(op))

        if pwr is not None:
            self.powerOnTime = timedelta(minutes=long(pwr))

        if cut is not None:
            self.cuttingTime = timedelta(seconds=long(cut))

        if run is not None:
            self.runTime= timedelta(seconds=long(run))

    def set_feedrate_nck(self, feed):
        if feed is not None:
            self.feedRateNck = feed

    def set_vel(self, x, y, z, count):
        if count is not None:
            if count > self.velCount:
                self.velCount = count

                if x is not None:
                    self.velX = x

                if y is not None:
                    self.velY = y

                if z is not None:
                    self.velZ = z

    def check_report_date(self):
        if not self.currentReport.is_today_report():
            self.currentReport.save_report()
            self.currentReport = CurrentReport()

    posX = 0.0
    posY = 0.0
    posZ = 0.0

    spindleLoad = 0.0
    spindleSpeed = 0.0

    reqParts = 0.0
    totalParts = 0.0

    progsEnded = 0
    progStatus = 0

    lastAlarm = 0
    actualAlarm = 0
    alarmTime = None

    operatingTime = timedelta()
    powerOnTime = timedelta()
    cuttingTime = timedelta()
    runTime = timedelta()

    feedRateNck = 0.0

    velX = 0.0
    velY = 0.0
    velZ = 0.0
    velCount = -1

    currentReport = None



