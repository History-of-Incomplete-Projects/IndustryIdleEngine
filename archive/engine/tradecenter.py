from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from engine.sql import BASE, session


class TradeCenterHistory(BASE):
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


    def get_all(raw_only: bool = False) -> list:
        if not raw_only:
            return session.query(TradeCenterHistory).all()
        if raw_only:
            return session.query(TradeCenterHistory).filter(TradeCenterHistory.Oil==None).all()
    

    def raw_to_detail() -> None:
        found_name = False
        found_price = False
        name = ""
        price = ""


        for row in TradeCenterHistory.get_all(raw_only=True):
            soup = BeautifulSoup(row.raw, "html.parser")
            for div1 in soup.find_all('div', class_="two-col"):
                for div2 in div1.find_all('div'):
                    if div2.has_attr("class") and not found_price: # right column
                        for div3 in div2.find_all('div'):
                            if not div3.has_attr("class") and not found_price:
                                for div4 in div3.find_all('div'):
                                    if not div4.has_attr("class") and not found_price:
                                        price = div4.text
                                        found_price = True
                    else: # left column
                        for div3 in div2.find_all('div'):
                            if not div3.has_attr("class") and not found_name:
                                name = div3.text
                                found_name = True
                
                if found_price and found_name:
                    setattr(row, name.replace(" ", ""), price)
                
                found_name = False
                found_price = False
                name = ""
                price = ""
        
        session.commit()


