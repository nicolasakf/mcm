from .. import db
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import INTEGER, TEXT
from flask_login import UserMixin


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


class UserSession(UserMixin, db.Model):
    __tablename__ = 'user_session'

    _id = Column('id', INTEGER, primary_key=True)
    name = Column(TEXT, unique=True)
