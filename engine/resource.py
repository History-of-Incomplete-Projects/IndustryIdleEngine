from dbmanager import *

from engine.managers import db_manager


class Resource(db_manager.Base):
    __tablename__ = "Resource"
    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

    UniqueConstraint('Name')


class ResourceManager:
    def __init__(self) -> None:
        self.db_manager = db_manager
    
    def get_or_create(self, name: str):
        return self.db_manager.get_or_create(
            Resource,
            Name=name
        )

    def get_by_name(self, name: str) -> Resource:
        return self.db_manager.get_first(
            Resource,
            Name=name
        )

    def get_by_id(self, id: int) -> Resource:
        return self.db_manager.get_first(
            Resource,
            id=id
        )
