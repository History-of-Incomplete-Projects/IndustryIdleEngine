from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    'sqlite:///game_play.db',
    connect_args={"check_same_thread": False}
)
BASE = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Backup(BASE):
    __tablename__ = "Backup"
    id = Column(Integer, primary_key=True)
    raw = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


def create_all() -> None:
    BASE.metadata.create_all(engine)

def add_object(obj) -> None:
    session.add(obj)
    session.commit()