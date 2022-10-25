from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

postgresql = {
    'pguser'  : 'root',
    'pgpasswd': 'admin',
    'pghost'  : 'postgres',
    'pgport'  : '5432',
    'pgdb'    : 'tool-conversion',
}

def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)

    engine = create_engine(url)
    return engine

def get_engine_from_settings():
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in postgresql.keys()):
        raise Exception('Bad config file')

    return get_engine(postgresql['pguser'], postgresql['pgpasswd'], postgresql['pghost'], postgresql['pgport'], postgresql['pgdb'])

def get_session():
    engine  = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session

session = get_session()