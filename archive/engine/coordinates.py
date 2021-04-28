from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


ARBITRARY = Coordinate(800, 550)
HOME = Coordinate(1300, 1000)
LEFT_MENU = Coordinate(200, 600)
HQ = Coordinate(670, 550)
TEADE_CENTER = Coordinate(720, 550)
HQ.EXPORT = Coordinate(100, 880)
HTML_BODY = Coordinate(1700, 160)
LEFT_MENU.EXIT = Coordinate(370, 110)
DRAG_START = Coordinate(680, 550)
DRAG_DOWN_END = Coordinate(680, 1000)
DRAG_UP_END = Coordinate(680, 110)