from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QDesktopWidget, QTableWidgetItem, \
    QTableWidget, QMainWindow, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QWidget

from engine.map import Oslo, Tile

APP_WIDTH = 1920
APP_HEIGHT = 1080


class DataTable(QMainWindow):
    def __init__(self) -> None:
        # Call the parent constructor
        super().__init__()

        # Set the size and title of the window
        self.setMinimumSize(QSize(APP_WIDTH, APP_HEIGHT))

        # Create the table with necessary properties
        self.table = QTableWidget(self)
        self.table.setColumnCount(Oslo.get_width())
        self.table.setRowCount(Oslo.get_height())
        self.table.setMinimumWidth(APP_WIDTH)
        self.table.setMinimumHeight(APP_HEIGHT)
        self.table.setFont(QFont('Arial', 8))

    def display(self) -> None:
        # Display the table
        self.table.show()

        # Display the window in the center of the screen
        win = self.frameGeometry()
        pos = QDesktopWidget().availableGeometry().center()
        win.moveCenter(pos)
        self.move(win.topLeft())
        self.show()

    def update(self, items: list) -> None:
        if len(items) == 1:
            self.__update_single(items[0])
        if len(items) > 1:
            self.__update_multiple(items)
        # Resize of the rows and columns based on the content
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def __update_single(self, item: str) -> None:
        # Set the table values
        modifiers = Tile.get_modifiers(item)
        for modifier in modifiers:
            self.__add_item(modifier.y, modifier.x, getattr(modifier, item))

    def __update_multiple(self, items: list):
        ...

    def __add_item(self, y: int, x: int, text: str) -> None:
        cell = QTableWidgetItem(text)
        if text:
            if (float(text.strip('%'))/100) >= 0:
                cell.setForeground(QBrush(QColor(0, 255, 0)))
            else:
                cell.setForeground(QBrush(QColor(255, 0, 0)))
        self.table.setItem(y, x, cell)


class Selection(QWidget):
    def __init__(self, parent=None) -> None:
        super(Selection, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 211, 291))
        
        for name in Tile.column_names():
            self.listWidget.addItem(QListWidgetItem(name))
        self.listWidget.itemClicked.connect(self.printItemText)
        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)
    
    def printItemText(self) -> None:
        items = self.listWidget.selectedItems()
        selected = []
        for item in items:
            selected.append(item.text())

        table.update(selected)


def app() -> None:
    global table
    app = QApplication([])
    mainWindow = QMainWindow()
    layout = QVBoxLayout()
    
    table = DataTable()
    table.update(['OilWell'])
    table.display()

    selection = Selection()
    selection.show()

    layout.addWidget(table)
    layout.addWidget(selection)

    mainWindow.setLayout(layout)

    app.exec()