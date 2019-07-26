# !/bin/python
# -*- coding: utf-8 -*-
from app.models.models import Machine
from app import db
from app import db_lib


def main():
    clean_db()
    create_machines()


def clean_db():
    Machine.query.delete()
    db.session.commit()


def create_machines():
    query = 'select * from insper.machine'
    data = db_lib.select(query)
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
            serial=str(r['machine_id'])
        )
        out.append(add_to_db(machine))

    return out


def add_to_db(obj):
    db.session.add(obj)
    db.session.flush()
    db.session.refresh(obj)
    db.session.commit()

    return obj._id


if __name__ == "__main__":
    main()
