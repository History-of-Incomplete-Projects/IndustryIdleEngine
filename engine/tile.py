from engine.parser import Parser
from engine.dbmanager import *
from engine.managers import db_manager, coordinate_manager
from engine.managers import player_manager, building_manager
from engine.building import Building
from engine.map import Coordinate
from engine.manager import Manager

class Tile(db_manager.Base):
    id = Column(Integer, primary_key=True)
    CoordinateId = Column(Integer, ForeignKey("Coordinate.id"))
    Raw = Column(String)
    BuildingId = Column(Integer, ForeignKey("Building.id"))
    Level = Column(Integer)
    TotalModifier = Column(Float)

    UniqueConstraint('Coordinate')


class TileManager(Manager):
    def __init__(self):
        self.db_manager = db_manager
        self.coordinate_manager = coordinate_manager
        self.player_manager = player_manager
        self.building_manager = building_manager

    def level_up(self, x, y, increment=1):
        tile = self.db_manager.get_all(Tile, X=x, Y=y)
        new = tile.Level + increment
        self.set_level(x, y, new)

    def set_level(self, x, y, new):
        self.db_manager.update(Tile, filters={"X": x, "Y": y}, updates={"Level": new})

    def create(self, reset: bool=True):
        if reset:
            self.db_manager.clear(Tile)
        for coordinate in self.db_manager.get_all(Coordinate):
            self.db_manager.get_or_create(Tile, CoordinateId=coordinate.id)

    def get_one(self, coordinate: Coordinate) -> Tile:
        return self.db_manager.get_first(Tile, CoordinateId=coordinate.id)

    def is_occupied(self, coordinate: Coordinate):
        tile = self.get_one(CoordinateId=coordinate.id)
        if tile.BuildingId:
            return tile, True
        return tile, False

    def update_modifier(self, coordinate: Coordinate, new_modifier: float) -> Tile:
        self.db_manager.update(Tile, filters={"CoordinateId": coordinate.id}, updates={"TotalModifier": new_modifier})

    def build(self, coordinate: Coordinate, building: Building) -> Tile:
        tile = self.get_one(Tile, CoordinateId=coordinate.id)
        updates = {
            "BuildingId": building.id,
            "Level": 1,
            "TotalModifier": Parser.tile_attribute(tile, building)
        }
        for neighbour in self.neighbours(coordinate):
            if neighbour.BuildingId == building.id:
                updates["TotalModifier"] += 10
                self.update_modifier(neighbour.CoordinateId, neighbour.TotalModifier+10)
        
        self.db_manager.update(Tile, filters={
            "CoordinateId": coordinate.id}, updates=updates)
        
    def neighbours(self, coordinate: Coordinate) -> list:
        neighbour_coordinates = (
            (coordinate.X, coordinate.Y-1), (coordinate.X, coordinate.Y+1),
            (coordinate.X-1, coordinate.Y), (coordinate.X+1, coordinate.Y)
        )
        neighbours = []
        for (x, y) in neighbour_coordinates:
            neighbour_coordindate = self.coordinate_manager.get_coord(x, y)
            neighbours.append(self.get_one(Tile, CoordinateId=neighbour_coordindate.id))
        return neighbours

    def get_real_modifier(self, coordinate: Coordinate) -> float:
        tile, is_occupied = self.is_occupied(coordinate)
        if not is_occupied:
            return 0.0
        player = self.player_manager.get()
        modifier = (
            self.get_real_modifier(coordinate) + player.ExtraAdjacentBonus
        ) * player.ProductionMultiplier
        return modifier

    def get_real_productions(self, coordinate: Coordinate) -> set:
        tile, is_occupied = self.is_occupied(coordinate)
        if not is_occupied:
            return 0.0
        real_modifier = self.get_real_modifier(coordinate)
        outputs = self.building_manager.get_outputs_by_building_id(tile.BuildingId)
        productions = []
        for output in outputs:
            productions.append((output.ResourceId, output.Production * real_modifier))
        return set(productions)

    def get_real_consumptions(self, coordinate: Coordinate) -> set:
        tile, is_occupied = self.is_occupied(coordinate)
        if not is_occupied:
            return 0.0
        real_modifier = self.get_real_modifier(coordinate)
        inputs = self.building_manager.get_inputs_by_building_id(tile.BuildingId)
        consumptions = []
        for input in inputs:
            consumptions.append((input.ResourceId, input.Consumption * real_modifier))
        return set(consumptions)
