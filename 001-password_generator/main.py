import sys
from PyQt6.QtWidgets import QApplication
from app import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.set_style(app)
window.show()

app.exec()
