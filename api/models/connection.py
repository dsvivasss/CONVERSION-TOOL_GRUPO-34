from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy

connector = Connector()


def getconn() -> pg8000.dbapi.Connection:
    conn: pg8000.dbapi.Connection = connector.connect(
        "convertor-tool:us-east4:tool-conversion",  # Cloud SQL Instance Connection Name
        "pg8000",
        user="postgres",
        password="root",
        db="tool-conversion"
    )
    return conn


def get_engine():
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,

    )
    return pool


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session


session = get_session()
