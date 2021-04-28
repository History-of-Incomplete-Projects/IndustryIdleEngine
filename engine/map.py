from types import SimpleNamespace
import json

from engine.dbmanager import *
from engine.managers import db_manager


class Coordinate(db_manager.Base):
    id = Column(Integer, primary_key=True)
    X = Column(Integer)
    Y = Column(Integer)

    UniqueConstraint("X", "Y")


class Map(db_manager.Base):
    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Width = Column(Integer)
    Height = Column(Integer)


class CoordinateManager:
    def __init__(self) -> None:
        self.db_manager = db_manager

    def build(self) -> None:
        map = self.db_manager.get_all(Map)[0]
        for x in range(0, map.X):
            for y in range(0, map.Y):
                self.db_manager.get_or_create(Coordinate, X=x, Y=y)

    def get_coord(self, x: int, y: int) -> Coordinate:
        return self.db_manager.get_first(Coordinate, X=x, Y=y)


class MapManager:
    def __init__(self) -> None:
        self.db_manager = db_manager
    
    def build(self, name: str = "Oslo") -> None:
        with open('./maps.json') as f:
            raw_data = json.load(f)
            map = raw_data[name]
            self.db_manager.clear(Map)
            self.db_manager.get_or_create(Map, 
                Name=name, Width=map["Width"], Height=map["Height"])
            