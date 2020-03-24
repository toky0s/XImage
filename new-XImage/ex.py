import sys
from PyQt5 import QtWidgets

class gridlayout_example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.grid_layout = QtWidgets.QGridLayout()

        self.label1 = QtWidgets.QLabel("label1",self)
        self.grid_layout.addWidget(self.label1,0,0,1,3)

        self.line_edit1 = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit1,1,0,1,3)

        self.label2 = QtWidgets.QLabel("label2",self)
        self.grid_layout.addWidget(self.label1,2,0,1,3)

        self.line_edit2 = QtWidgets.QLineEdit(self)
        self.grid_layout.addWidget(self.line_edit2,3,0,1,3)

        self.button1 = QtWidgets.QPushButton("button1",self)
        self.button2 = QtWidgets.QPushButton("button2",self)
        self.button3 = QtWidgets.QPushButton("button3",self)

        self.grid_layout.addWidget(self.button1, 4,0,1,1)
        self.grid_layout.addWidget(self.button2, 4,1,1,1)
        self.grid_layout.addWidget(self.button3, 4,2,1,1)

        self.setLayout(self.grid_layout)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = gridlayout_example()
    sys.exit(app.exec_())