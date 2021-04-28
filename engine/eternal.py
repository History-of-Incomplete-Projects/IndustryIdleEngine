from engine.map import Coordinate
from engine.building import Building
from engine.managers import *


class EngineEternal:
    def __init__(self) -> None:
        self.building_manager = building_manager
        self.db_manager = db_manager
        self.resource_manager = resource_manager
        self.tile_manager = tile_manager
        self.map_manager = map_manager
        self.coordinate_manager = coordinate_manager
        self.player_manager = player_manager

    def dependents(self, building: Building) -> dict:
        ...

    def clusters(self, building: Building, min: int = 3) -> list:
        ...

    def best_locations(self, building: Building, max_level: int, min_production: int, exclude: list = None) -> list:
        ...

    def best_competitive_locations(self, competitors={}) -> dict:
        occupied = []
        for competitor in competitors:
            building = self.building_manager.get_by_id(competitor["id"])
            best_locations = self.best_locations(
                building, competitor["max_level"], competitor["min_production"]
            )
            for location in best_locations:
                if location in occupied:
                    ...


engine_eternal = EngineEternal()