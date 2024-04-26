from datetime import datetime
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import (
    QLineEdit,
    QTreeWidget,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTreeWidgetItem,
    QApplication,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.shortcut = QShortcut(QKeySequence("Return"), self)

        self.entry = QLineEdit()
        self.list_box = QTreeWidget()

        self.add_btn = QPushButton("Add")
        self.remove_btn = QPushButton("Remove")

        self.layout = QVBoxLayout()
        self.hor_layout = QHBoxLayout()

        self.set_window()
        self.load_from_file()

    @staticmethod
    def create_new_item(checked: bool, text: str, date: str) -> QTreeWidgetItem:
        """Create new QTreeWidgetItem"""

        new_item = QTreeWidgetItem()

        new_item.setCheckState(0, Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        new_item.setText(1, text)
        new_item.setText(2, date)

        return new_item

    @staticmethod
    def from_check_state_to_bool(check_state: Qt.CheckState) -> str:
        """Convert CheckState to boolean"""

        return "True" if check_state == Qt.CheckState.Checked else "False"

    @staticmethod
    def read_file(file_name: str) -> list:
        with open(file_name, 'r') as file:
            return file.readlines()

    @staticmethod
    def overwrite_file(file_name: str, data: list) -> None:
        with open(file_name, 'w') as file:
            file.write(''.join(data))

    @staticmethod
    def set_style(app: QApplication) -> None:
        """Styles for window"""

        with open("styles.qss", 'r') as file:
            styles = file.read()

        app.setStyleSheet(styles)

    @staticmethod
    def set_font(item: QTreeWidgetItem, state: bool) -> None:
        """Set font style for text as needed"""

        font = item.font(1)
        font.setStrikeOut(True if state else False)
        font.setItalic(True if state else False)
        item.setFont(1, font)

    def set_window(self) -> None:
        """Set all widgets"""

        self.setWindowTitle("TodoList")
        self.setFixedSize(QSize(500, 400))
        self.setWindowIcon(QIcon("resources/icon.png"))

        self.shortcut.activated.connect(self.click_add)

        self.list_box.setColumnCount(3)
        self.list_box.setColumnWidth(1, 250)
        self.list_box.setHeaderLabels(["Done", "Name", "DateTime"])
        self.list_box.itemChanged.connect(self.change_check_state)

        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self.click_add)

        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self.click_remove)

        self.setLayout(self.layout)
        self.layout.addWidget(self.list_box)
        self.layout.addWidget(self.entry)
        self.hor_layout.addWidget(self.add_btn)
        self.hor_layout.addWidget(self.remove_btn)
        self.layout.insertLayout(2, self.hor_layout)

    def delete_from_file(self, index: int) -> None:
        file_data = self.read_file("todo-list.txt")

        with open("todo-list.txt", 'w') as file:
            for item_index, item in enumerate(file_data):
                if item_index == index:
                    continue

                file.write(item)

    def click_add(self) -> None:
        """Handler for button -> Add"""

        text = self.entry.text()

        if not text:
            return

        self.adding_new_item(text)
        self.save_to_file()
        self.entry.setText('')

    def check_duplicate(self, text: str) -> None:
        """Check duplicate in list"""

        file_data = self.read_file("todo-list.txt")

        for index, line in enumerate(file_data):
            if text == line.split(',')[1]:
                file_data[index] = ''
                break

        self.overwrite_file("todo-list.txt", file_data)
        self.list_box.clear()
        self.load_from_file()

    def adding_new_item(self, text: str) -> None:
        """Add new item and scroll to him"""

        self.check_duplicate(text)
        item = self.create_new_item(False, text, datetime.now().strftime("%m-%d %H:%M"))

        self.list_box.addTopLevelItem(item)
        self.list_box.scrollToItem(item)

    def delete_item(self, item: QTreeWidgetItem) -> None:
        index = self.list_box.indexOfTopLevelItem(item)
        self.delete_from_file(index)
        self.list_box.takeTopLevelItem(index)

    def click_remove(self) -> None:
        """Handler for button -> Remove"""

        item = self.list_box.selectedItems()

        if not item:
            return

        self.delete_item(item[0])

    def get_last_index(self) -> int:
        """Get index of last item"""

        return self.list_box.topLevelItemCount() - 1

    def get_item_info(self, item: QTreeWidgetItem) -> str:
        """Get item data"""

        item_check_state = self.from_check_state_to_bool(item.checkState(0))
        item_text = item.text(1)
        item_datetime = item.text(2)

        return ','.join([item_check_state, item_text, item_datetime, '\n'])

    def save_to_file(self) -> None:
        last_index = self.get_last_index()
        item = self.list_box.topLevelItem(last_index)

        with open("todo-list.txt", 'a') as file:
            file.write(self.get_item_info(item))

    def load_from_file(self) -> None:
        with open("todo-list.txt", 'r') as file:
            for line in file:
                check_state, text, date, _ = line.split(',')

                new_item = self.create_new_item(eval(check_state), text, date)
                self.set_font(new_item, eval(check_state))

                self.list_box.addTopLevelItem(new_item)
                self.list_box.scrollToItem(new_item)

    def change_check_state(self, item: QTreeWidgetItem) -> None:
        """Change CheckState in file"""

        state = eval(self.from_check_state_to_bool(item.checkState(0)))
        self.set_font(item, state)
        item_text = item.text(1)

        file_data = self.read_file("todo-list.txt")

        for index, line in enumerate(file_data):
            if item_text in line:
                file_data[index] = self.get_item_info(item)

        self.overwrite_file("todo-list.txt", file_data)
