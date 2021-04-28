from bs4 import BeautifulSoup

from engine.tile import Tile
from engine.building import Building
from engine.tradecenter import TradeCenterHistory

class Parser:
    def tile_attributes(tile: Tile) -> dict:
        attributes = {}

        found_name = False
        found_modifier = False
        found_inputs = False
        found_outputs = False
        name = ""
        modifier = ""
        inputs = []
        outputs = []

        soup = BeautifulSoup(tile.raw, "html.parser")
        for div1 in soup.find_all('div', class_="row"):
            for div2 in div1.find_all('div', class_="f1 pointer"):
                for div3 in div2.find_all('div', class_="", recursive=False): # Name
                    name = div3.text
                    found_name = True
                    for span in div3.find_all('span'): # Modifier
                        name = name.replace(span.text, "")
                        if span['class'] == ['text-m', 'ml5', 'green'] or \
                            span['class'] == ['text-m', 'ml5', 'red']:
                            modifier = span.text
                            found_modifier = True
                for div3 in div2.find_all('div', class_="text-desc text-s row"): # inputs & outputs
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
            
            if found_modifier and found_name:
                attributes[name] = {
                    "modifier": modifier,
                }
            if found_outputs and found_name:
                attributes[name] = {
                    "outputs": outputs,
                }
            if found_inputs and found_name:
                attributes[name] = {
                    "inputs": inputs,
                }
            
            found_name = False
            found_modifier = False
            found_inputs = False
            found_outputs = False
            name = ""
            modifier = ""
            inputs = []
            outputs = []

        return attributes

    def tile_attribute(tile: Tile, building: Building) -> int:
        return Parser.tile_attributes(tile)[building.Name]

    def trade_center_attributes() -> tuple:
        found_name = False
        found_price = False
        names = []
        prices = []

        for row in TradeCenterHistory.get_all(raw_only=True):
            soup = BeautifulSoup(row.raw, "html.parser")
            for div1 in soup.find_all('div', class_="two-col"):
                for div2 in div1.find_all('div'):
                    if div2.has_attr("class") and not found_price: # right column
                        for div3 in div2.find_all('div'):
                            if not div3.has_attr("class") and not found_price:
                                for div4 in div3.find_all('div'):
                                    if not div4.has_attr("class") and not found_price:
                                        prices.append(div4.text)
                                        found_price = True
                    else: # left column
                        for div3 in div2.find_all('div'):
                            if not div3.has_attr("class") and not found_name:
                                names.append(div3.text)
                                found_name = True
                
                if found_price and found_name:
                    setattr(row, name.replace(" ", ""), price)
                
                found_name = False
                found_price = False
                name = ""
                price = ""
        
        return names, prices