from dbmanager import *

from engine.managers import db_manager

class Player(db_manager.Base):
    id = Column(Integer, primary_key=True)
    ProductionMultiplier = Column(Integer)
    ExtraAdjacentBonus = Column(Integer)


class PlayerManager:
    def __init__(self) -> None:
        self.db_manager = db_manager
    
    def create(self, ProductionMultiplier: int = 0, ExtraAdjacentBonus: int = 0) -> None:
        self.clear()
        self.db_manager.create_object(
            Player, ProductionMultiplier=ProductionMultiplier, 
            ExtraAdjacentBonus=ExtraAdjacentBonus
        )

    def update(self, ProductionMultiplier: int = 0, ExtraAdjacentBonus: int = 0) -> None:
        self.db_manager.update(Player, update={
            "ProductionMultiplier": ProductionMultiplier, 
            "ExtraAdjacentBonus": ExtraAdjacentBonus
        })

    def get(self) -> Player:
        return self.db_manager.get_first(Player)
    
    def clear(self):
        self.db_manager.clear()