from sqlalchemy import Column, Integer, String, UniqueConstraint
from bs4 import BeautifulSoup

from engine.dbmanager import *
from engine.managers import db_manager

class Tile(Base):
    __tablename__ = "Tile"
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    raw = Column(String)
    NaturalGasPump = Column(String)
    OilWell = Column(String)
    AluminumMine = Column(String)
    IronMine = Column(String)
    LoggingCamp = Column(String)
    CoalMine = Column(String)
    SiliconMine = Column(String)
    OilRefinery = Column(String)
    PowerBank = Column(String)
    SolarPanel = Column(String)
    WindTurbine = Column(String)
    GasPowerPlant = Column(String)
    GasProcessingPlant = Column(String)
    PaperMill = Column(String)
    BatteryFactory = Column(String)
    Polytechnic = Column(String)
    GlassFactory = Column(String)
    SemiconductorFactory = Column(String)
    ClothingFactory = Column(String)
    CircuitFoundry = Column(String)
    ShoeFactory = Column(String)
    ToyFactory = Column(String)
    ScreenFactory = Column(String)
    CameraFactory = Column(String)
    School = Column(String)
    BookPublisher = Column(String)
    FashionFactory = Column(String)
    ComputerFactory = Column(String)
    PhoneFactory = Column(String)
    VideoFarm = Column(String)
    MovieStudio = Column(String)
    BitcoinFarm = Column(String)
    DogecoinFarm = Column(String)
    SoftwareCompany = Column(String)
    PetrolPowerPlant = Column(String)
    ChromiumAlloyPlant = Column(String)
    CoalPowerPlant = Column(String)
    LumberMill = Column(String)
    SteelMill = Column(String)
    TitaniumAlloyPlant = Column(String)
    UraniumEnrichmentPlant = Column(String)
    NuclearPowerPlant = Column(String)
    Colosseum = Column(String)
    DrumFactory = Column(String)
    EngineFactory = Column(String)
    GunFactory = Column(String)
    GuitarFactory = Column(String)
    RobotFactory = Column(String)
    ArtilleryFactory = Column(String)
    JetEngineFactory = Column(String)
    MissileFactory = Column(String)
    CarFactory = Column(String)
    TankFactory = Column(String)
    RocketFactory = Column(String)
    AircraftFactory = Column(String)
    SatelliteFactory = Column(String)
    SpaceshipFactory = Column(String)
    OperatingSystemInc = Column(String)
    WebBrowser = Column(String)
    SpaceStationFactory = Column(String)

    UniqueConstraint('x', 'y', name='coord')

    def get_all(raw_only: bool = True) -> list:
        if not raw_only:
            return db_manager.session.query(Tile).all()
        if raw_only:
            return db_manager.session.query(Tile).filter(Tile.OilRefinery==None).all()
            

    def get_first():
        return db_manager.session.query(Tile).first()


    def raw_to_detail() -> None:
        found_name = False
        found_modifier = False
        name = ""
        modifier = ""


        for row in Tile.get_all(raw_only=True):
            soup = BeautifulSoup(row.raw, "html.parser")
            for div1 in soup.find_all('div', class_="row"):
                for div2 in div1.find_all('div', class_="f1 pointer"):
                    for div3 in div2.find_all('div', class_="", recursive=False):
                        name = div3.text
                        found_name = True
                        for span in div3.find_all('span'):
                            name = name.replace(span.text, "")
                            if span['class'] == ['text-m', 'ml5', 'green'] or \
                                span['class'] == ['text-m', 'ml5', 'red']:
                                modifier = span.text
                                found_modifier = True
                
                if found_modifier and found_name:
                    setattr(row, name.replace(" ", ""), modifier)
                
                found_name = False
                found_modifier = False
                name = ""
                modifier = ""

        db_manager.session.commit()
    
    def column_names(building_only: bool = True) -> list:
        columns = Tile.__table__.columns.keys()
        if building_only:
            columns.remove('id')
            columns.remove('x')
            columns.remove('raw')
            columns.remove('y')
            return columns
        else:
            return columns
    
    def get_modifiers(building) -> list:
        return db_manager.session.query(Tile.x, Tile.y, getattr(Tile, building)).all()


class Oslo(Base):
    __tablename__ = "Oslo"
    id = Column(Integer, primary_key=True)
    height = Column(Integer, default=50)
    width = Column(Integer, default=50)


    def get_row():
        return db_manager.session.query(Oslo).first()

    def get_height():
        return db_manager.session.query(Oslo).first().height

    def get_width():
        return db_manager.session.query(Oslo).first().width