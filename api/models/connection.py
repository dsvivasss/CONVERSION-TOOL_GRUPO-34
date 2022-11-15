from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
import os

connector = Connector()

project_id = os.environ['proyect-id']
zone = os.environ['zone']
instance_name = os.environ['instance_name']
db_user=os.environ['db_user']
db_password=os.environ['db_password']
db_name= os.environ['db_name']


def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        f"{project_id}:{zone}:{instance_name}",  # Cloud SQL Instance Connection Name
        "pg8000",
        user=db_user,
        password=db_password,
        db=db_name
    )
    return conn


def get_engine():
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size = 300,
        pool_timeout= 1
    )
    return pool


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session


session = get_session()