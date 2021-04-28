from dbmanager import DBManager

from engine.building import BuildingManager
from engine.resource import ResourceManager
from engine.tile import TileManager
from engine.map import MapManager, CoordinateManager
from engine.player import PlayerManager


building_manager = BuildingManager()
db_manager = DBManager()
resource_manager = ResourceManager()
tile_manager = TileManager()
map_manager = MapManager()
coordinate_manager = CoordinateManager()
player_manager = PlayerManager()