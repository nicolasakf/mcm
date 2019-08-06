# !/bin/python
# -*- coding: utf-8 -*-
from app.models.models import Machine
from app import db
from app import db_lib


def clean_db():
    """
    Cleans database for selected user
    :return: void;
    """
    Machine.query.delete()
    db.session.commit()


def create_machines(user_id):
    """
    Initializes machines to local instance
    :param user_id: int;
    :return: list; list of Machine objects
    """
    data = db_lib.get_machine_list(user_id)
    out = []
    for i, r in data.iterrows():
        machine = Machine(
            name=str(r['name']),
            pn=str(r['pn']),
            scc=str(r['scc']),
            celula=str(r['celula']),
            cnc=str(r['cnc']),
            cnc_sw_ver=str(r['cnc_sw_ver']),
            mon_hw_ver=str(r['mon_hw_ver']),
            mon_sw_ver=str(r['mon_sw_ver']),
            img_filename=str(r['img_filename']),
            manual_filename=str(r['manual_filename']),
            serial=str(r['machine_id']),
            # user_id=user_id
        )
        out.append(add_to_db(machine))

    return out


def add_to_db(obj):
    """
    Adds machine instance to local database
    :param obj: Machine;
    :return: int; instance id
    """
    db.session.add(obj)
    db.session.flush()
    db.session.refresh(obj)
    db.session.commit()

    return obj._id
