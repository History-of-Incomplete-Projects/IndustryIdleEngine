from datetime import datetime
from dbmanager import *

from engine.managers import db_manager


class TradeCenterHistory(db_manager.Base):
    __tablename__ = "Trade Center History"
    id = Column(Integer, primary_key=True)
    raw = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    Aluminum = Column(String)
    Battery = Column(String)
    Bitcoin = Column(String)
    Book = Column(String)
    Camera = Column(String)
    Clothes = Column(String)
    Coal = Column(String)
    Dogecoin = Column(String)
    Fashion = Column(String)
    Iron = Column(String)
    NaturalGas = Column(String)
    Glass = Column(String)
    IntegratedCircuit = Column(String)
    Movie = Column(String)
    Oil = Column(String)
    PC = Column(String)
    Paper = Column(String)
    Petrol = Column(String)
    Phone = Column(String)
    Plastic = Column(String)
    Screen = Column(String)
    Semiconductor = Column(String)
    Shoes = Column(String)
    Silicon = Column(String)
    Software = Column(String)
    Toy = Column(String)
    Video = Column(String)
    Wood = Column(String)