from string import ascii_letters, digits, punctuation
from random import choices

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QSlider,
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit
)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.difficult_password = 1

        """Creating widgets"""
        self.layout = QVBoxLayout()
        self.labelDifficult = QLabel(f"Difficult of the password: {self.difficult_password}")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.button = QPushButton("Generate")
        self.password_line = QLineEdit(self)

        self.set_window()

    def set_window(self) -> None:
        """Widgets settings"""

        self.setWindowTitle("Password Generator")
        self.setFixedSize(QSize(350, 220))

        self.setLayout(self.layout)

        self.slider.actionTriggered.connect(self.slider_move)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setSingleStep(1)

        self.button.clicked.connect(self.password_generate)

        self.password_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_line.setReadOnly(True)
        self.password_line.setVisible(False)

        self.layout.addWidget(self.labelDifficult)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.password_line)

    @staticmethod
    def set_style(app: QApplication) -> None:
        """Styles for app"""

        with open("style_sheets.txt", 'r') as file:
            app.setStyleSheet(''.join(file.readlines()))

    def slider_move(self) -> None:
        """Slider handler"""

        self.password_line.setVisible(False) if self.password_line.isVisible() else ...
        self.difficult_password = self.slider.value()
        self.labelDifficult.setText(f"Difficult of the password: {self.difficult_password + 1}")

    def password_generate(self) -> None:
        """Btn_click handler - password generator"""

        self.password_line.setVisible(True)
        password = ''.join(choices(ascii_letters + punctuation + digits, k=self.difficult_password))
        self.password_line.setText(password)
