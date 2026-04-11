import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout
from main import main


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Selector")

        layout = QVBoxLayout()

        btn = QPushButton("Wybierz folder")
        btn.clicked.connect(self.select_folder)

        layout.addWidget(btn)
        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Wybierz folder")
        if folder:
            main(folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())