import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = '/var/tmp/romipiloto/uploads/'

CAM_STREAM = {
    '1': 'http://azdebian.omega7systems.com:6010/cam0.ogv',
    '2': 'http://azdebian.omega7systems.com:6010/cam1.ogv'
}
