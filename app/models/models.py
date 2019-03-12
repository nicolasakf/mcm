from .. import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import INTEGER, DATE, TIME, TEXT


class Report(db.Model):
    __tablename__ = 'report'

    _id = Column('id', INTEGER, primary_key=True)
    date = Column(DATE)
    resp_name = Column(TEXT)
    prod_amount_t1 = Column(INTEGER)
    prod_amount_t2 = Column(INTEGER)
    prod_amount_t3 = Column(INTEGER)
    op_amount_t1 = Column(INTEGER)
    op_amount_t2 = Column(INTEGER)
    op_amount_t3 = Column(INTEGER)
    idx_avail = Column(INTEGER)
    idx_perf = Column(INTEGER)
    idx_quality = Column(INTEGER)
    idx_oee = Column(INTEGER)
    machine_id = Column(INTEGER, ForeignKey('machine.id'))
    stops = relationship('MachineStop', backref='report', lazy='dynamic')


class MachineStop(db.Model):
    __tablename__ = "machine_stop"

    _id = Column('id', INTEGER, primary_key=True)
    turn_num = Column(INTEGER)  # 1 - turn1, 2 - turn2, 3 - turn3
    name = Column(TEXT)
    dateStart = Column(DATE)
    timeStart = Column(TIME)
    dateEnd = Column(DATE)
    timeEnd = Column(TIME)
    reason = Column(TEXT)
    report_id = Column(INTEGER, ForeignKey('report.id'))


class Machine(db.Model):
    __tablename__ = 'machine'

    _id = Column('id', INTEGER, primary_key=True)
    name = Column(TEXT)
    pn = Column(TEXT)
    scc = Column(TEXT)
    celula = Column(TEXT)
    cnc = Column(TEXT)
    cnc_sw_ver = Column(TEXT)
    mon_hw_ver = Column(TEXT)
    mon_sw_ver = Column(TEXT)
    img_filename = Column(TEXT)
    manual_filename = Column(TEXT)
    serial = Column(TEXT)
    reports = relationship('Report', backref='machine', lazy='dynamic')

