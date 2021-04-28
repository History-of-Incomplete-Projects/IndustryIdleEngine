from bs4 import BeautifulSoup
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint

from engine.sql import BASE, session, add_object
from engine.map import Tile

class Resource(BASE):
    __tablename__ = "Resource"
    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)


class BuildingInput(BASE):
    __tablename__ = "Building Input"
    id = Column(Integer, primary_key=True)
    BuildingId = Column(Integer, ForeignKey("Building.id"))
    ResourceId = Column(Integer, ForeignKey("Resource.id"))
    Consumption = Column(Integer)

    UniqueConstraint('BuildingId', 'ResourceId')


class BuildingOutput(BASE):
    __tablename__ = "Building Output"
    id = Column(Integer, primary_key=True)
    BuildingId = Column(Integer, ForeignKey("Building.id"))
    ResourceId = Column(Integer, ForeignKey("Resource.id"))
    Production = Column(Integer)

    UniqueConstraint('BuildingId', 'ResourceId')


class Building(BASE):
    __tablename__ = "Building"
    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)


def construct_buildings() -> None:
    found_name = False
    found_inputs = False
    found_outputs = False
    name = ""
    inputs = []
    outputs = []

    row = Tile.get_first()
    soup = BeautifulSoup(row.raw, "html.parser")
    for div1 in soup.find_all('div', class_="row"):
        for div2 in div1.find_all('div', class_="f1 pointer"):
            for div3 in div2.find_all('div', class_="", recursive=False):
                name = div3.text
                found_name = True
                for span in div3.find_all('span'):
                    name = name.replace(span.text, "")
            for div3 in div2.find_all('div', class_="text-desc text-s row"):
                text = div3.text
                if "login" in text: # input
                    text = text.replace("login", "")
                    inputs = text.split(", ")
                    for input in inputs:
                        inputs[inputs.index(input)] = input.split(" x")
                    found_inputs = True
                if "logout" in text: # output
                    text = text.replace("logout", "")
                    outputs = text.split(", ")
                    for output in outputs:
                        outputs[outputs.index(output)] = output.split(" x")
                    found_outputs = True
        
        if found_inputs and found_name and found_outputs and not name == "Power Bank":
            building = Building(Name=name)
            if not session.query(Building).filter_by(Name=name).first():
                add_object(building)
            building = session.query(Building).filter_by(Name=name).first()
            for input in inputs:
                resource = Resource(Name=input[0])
                if not session.query(Resource).filter_by(Name=input[0]).first():
                    add_object(resource)
                resource = session.query(Resource).filter_by(Name=input[0]).first()
                if not session.query(BuildingInput).\
                    filter_by(BuildingId=building.id, ResourceId=resource.id, Consumption=input[1]).first():
                    add_object(BuildingInput(BuildingId=building.id, ResourceId=resource.id, Consumption=input[1]))
            for output in outputs:
                resource = Resource(Name=output[0])
                if not session.query(Resource).filter_by(Name=output[0]).first():
                    add_object(resource)
                resource = session.query(Resource).filter_by(Name=output[0]).first()
                if not output[0] == "Power" and not session.query(BuildingOutput).\
                    filter_by(BuildingId=building.id, ResourceId=resource.id, Production=output[1]).first():
                    add_object(BuildingOutput(BuildingId=building.id, ResourceId=resource.id, Production=output[1]))
        
        found_name = False
        found_inputs = False
        found_outputs = False
        name = ""
        inputs = []
        outputs = []


    session.commit()
