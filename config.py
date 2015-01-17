import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = ';\x10\xea2\xd8\xbc[\xe7ax.\xe4\xa0"\xcf\x8c\xf3\xe62V\xe3Pd\xeb'

