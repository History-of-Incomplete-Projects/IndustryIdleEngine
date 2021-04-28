from engine.map import Oslo, Tile
import pyautogui
import win32clipboard

from engine.coordinates import ARBITRARY, Coordinate, DRAG_DOWN_END, DRAG_UP_END
from engine.coordinates import HOME, HQ, HTML_BODY, LEFT_MENU, TEADE_CENTER, DRAG_START
from engine.sql import Backup, session, add_object
from engine.tradecenter import TradeCenterHistory

def calibrate() -> None:
    click_on_home()
    zoom_out()
    zoom_in()


def move_mouse(loc: Coordinate) -> None:
    pyautogui.moveTo(loc.x, loc.y)


def zoom_out() -> None:
    move_mouse(ARBITRARY)
    pyautogui.scroll(-5000)


def zoom_in() -> None:
    move_mouse(ARBITRARY)
    pyautogui.scroll(500)


def click_on_home() -> None:
    move_mouse(HOME)
    pyautogui.leftClick()


def click_on_hq() -> None:
    move_mouse(HQ)
    pyautogui.leftClick()


def back_up_game() -> None:
    click_on_hq()
    left_menu_scroll_down()
    move_mouse(HQ.EXPORT)
    pyautogui.leftClick()
    pyautogui.sleep(5)
    add_object(Backup(raw=get_clipboard_data()))
    

def left_menu_scroll_down() -> None:
    move_mouse(LEFT_MENU)
    pyautogui.scroll(-1500)


def log_trade_center_history() -> None:
    move_mouse(TEADE_CENTER)
    pyautogui.leftClick()
    add_object(TradeCenterHistory(raw=get_raw_html_data()))
    TradeCenterHistory.raw_to_detail()


def get_raw_html_data() -> None:
    move_mouse(HTML_BODY)
    pyautogui.scroll(1500)
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.sleep(0.25)
    return get_clipboard_data()


def get_clipboard_data() -> str:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def get_tile_data(x: int, y: int) -> None:
    move_mouse(calculate_tile_position(x, y))
    pyautogui.leftClick()
    add_object(Tile(x=x, y=y, raw=get_raw_html_data()))
    move_mouse(LEFT_MENU.EXIT)
    pyautogui.leftClick()


def calculate_tile_position(x: int, y: int) -> Coordinate:
    if y <= 25:
        return Coordinate(
            x=13+x*27,
            y=113+y*27
        )
    else:
        return Coordinate(
            x=13+x*27,
            y=375+(y-26)*27
        )


def get_all_tile_data() -> None:
    zoom_out()
    move_mouse(DRAG_START)
    pyautogui.mouseDown(button='left')
    move_mouse(DRAG_DOWN_END)
    pyautogui.mouseUp(button='left')

    oslo = Oslo.get_row()
    for y in range(26, oslo.height):
        if y > 25: 
            move_mouse(DRAG_START)
            pyautogui.mouseDown(button='left')
            move_mouse(DRAG_UP_END)
            pyautogui.mouseUp(button='left')
        for x in range(0, oslo.width):
            if (y == 25 and x > 21 and x < 31):
                continue
            print("fetching data from: ", x, y)
            get_tile_data(x, y)

    Tile.raw_to_detail()


def Collect(new_map: bool = False) -> None:
    if new_map:
        get_all_tile_data()
        
    calibrate()
    back_up_game()

    log_trade_center_history()