#!../romipiloto_env/bin/python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db, directory='db/migrations/')

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models import models

if __name__ == '__main__':
    manager.run()
