from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

Engine = create_engine('sqlite:///filmfinder_tahelka.db', echo=True)
Session = sessionmaker(bind=Engine)

# To enforce Foreign Key constraints.
# @event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
