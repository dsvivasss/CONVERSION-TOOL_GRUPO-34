import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from environments import project_id, zone, instance_name, db_user, db_password, db_name

def getconn():
    with Connector() as connector:
        conn = connector.connect(
            f"{project_id}:{zone}:{instance_name}",  # Cloud SQL Instance Connection Name
            "pg8000",
            user=db_user,
            password=db_password,
            db=db_name,
            ip_type= IPTypes.PUBLIC
        )
        return conn
SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"
engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {
        "check_same_thread": False,
        "connect_timeout": 60},
    creator=getconn,
    pool_size=50,
    max_overflow=-1
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()