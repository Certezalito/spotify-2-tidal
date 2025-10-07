from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    item_type = Column(String)
    item_name = Column(String)
    artist_name = Column(String)
    album_name = Column(String)
    status = Column(String)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def get_db_session():
    """
    Returns a database session object.
    """
    engine = create_engine('sqlite:///synced.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
