from engine.dbmanager import *
from engine.resource import Resource
from engine.managers import db_manager, resource_manager

class BuildingInput(db_manager.Base):
    __tablename__ = "BuildingInput"
    id = Column(Integer, primary_key=True)
    BuildingId = Column(Integer, ForeignKey("Building.id"))
    ResourceId = Column(Integer, ForeignKey("Resource.id"))
    Consumption = Column(Integer)

    UniqueConstraint('BuildingId', 'ResourceId')


class BuildingOutput(db_manager.Base):
    __tablename__ = "BuildingOutput"
    id = Column(Integer, primary_key=True)
    BuildingId = Column(Integer, ForeignKey("Building.id"))
    ResourceId = Column(Integer, ForeignKey("Resource.id"))
    Production = Column(Integer)

    UniqueConstraint('BuildingId', 'ResourceId')


class Building(db_manager.Base):
    __tablename__ = "Building"
    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

    UniqueConstraint('Name')


class BuildingManager:
    def __init__(self) -> None:
        self.db_manager = db_manager
        self.resource_manager = resource_manager        
    
    def get_or_create(self, name: str, inputs: list, outputs: list) -> Building:
        for input in inputs:
            self.resource_manager.get_or_create(input["Name"])
        for output in outputs:
            self.resource_manager.get_or_create(output["Name"])
        instance, result = self.db_manager.get_or_create(
            Building,
            Name=name
        )
        if result:
            self.create_inputs(instance, inputs)
            self.create_outputs(instance, outputs)
        return instance

    def create_inputs(self, building: Building, inputs: list):
        for input in inputs:
            input["BuildingId"] = building.id
            self.db_manager.get_or_create(
                BuildingInput,
                **input
            )
    
    def create_outputs(self, building: Building, outputs: list):
        for output in outputs:
            output["BuildingId"] = building.id
            self.db_manager.get_or_create(
                BuildingOutput,
                **output
            )

    def create_building(self, name: str):
        return self.db_manager.create_object(
            Building,
            Name=name
        )

    def get_by_name(self, name: str) -> Building:
        return self.db_manager.get_first(
            Building,
            Name=name
        )

    def get_by_id(self, id: int) -> Building:
        return self.db_manager.get_first(
            Building,
            id=id
        )

    def get_inputs_by_building_name(self, name: str) -> list:
        building_id = self.get_by_name(name).id
        return self.get_inputs_by_building_id(building_id)

    def get_inputs_by_building_id(self, id: int) -> list:
        return self.db_manager.get_all(
            BuildingInput,
            BuildingId=id
        )

    def get_outputs_by_building_name(self, name: str) -> list:
        building_id = self.get_by_name(name).id
        return self.get_outputs_by_building_id(building_id)

    def get_outputs_by_building_id(self, id: int) -> list:
        return self.db_manager.get_all(
            BuildingOutput,
            BuildingId=id
        )

    def get_outputs_by_resource_name(self, name: str) -> list:
        building_id = self.get_outputs_by_resource_id(name).id
        return self.get_outputs_by_resource_id(building_id)

    def get_outputs_by_resource_id(self, id: int) -> list:
        return self.db_manager.get_all(
            BuildingOutput,
            ResourceId=id
        )
    
    def best_producer(self, resource: Resource) -> tuple(Building, int):
        best_output = self.db_manager.get_max(BuildingOutput, BuildingOutput.Production, ResourceId=resource.id)
        return self.get_by_id(best_output.BuildingId), best_output.Production
            