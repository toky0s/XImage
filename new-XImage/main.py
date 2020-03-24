from PyQt5.QtWidgets import (QWidget,QMainWindow, QApplication, QPushButton, 
QRadioButton, QLabel, QGridLayout, QCheckBox, QLineEdit, QFileDialog, QFontDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QFileDialog)
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from XImageClass import QHRadioGroupBox, QRadioButtonCustom


class App(QWidget):

    label_font = QFont('Consolas',10)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('new-XImage')
        # self.setGeometry(500,200,700,500)
        # self.setWindowIcon()
        self.setupUI()

    def setupUI(self):

        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)

        self.label_find = QLabel('Find:', self)
        self.grid_layout.addWidget(self.label_find,0,0)

        self.line_find = QLineEdit(self)
        self.line_find.setPlaceholderText('What do you want to find?')
        self.grid_layout.addWidget(self.line_find,0,1)

        self.label_page = QLabel('Page:', self)
        self.grid_layout.addWidget(self.label_page,1,0)

        self.line_page = QLineEdit(self)
        self.grid_layout.addWidget(self.line_page,1,1)

        self.label_per_page = QLabel('Per page:', self)
        self.grid_layout.addWidget(self.label_per_page,2,0)

        self.line_per_page = QLineEdit(self)
        self.grid_layout.addWidget(self.line_per_page,2,1)

        self.label_save_at = QLabel('Save at:', self)
        self.grid_layout.addWidget(self.label_save_at,3,0)

        self.btt_save_at_browse = QPushButton('Browse...')
        self.btt_save_at_browse.clicked.connect(self.browse)
        self.grid_layout.addWidget(self.btt_save_at_browse,3,2)

        self.line_save_at = QLineEdit(self)
        self.grid_layout.addWidget(self.line_save_at,3,1)
        
        self.radio_group_box_quality = QHRadioGroupBox('Quality')
        self.rd_quality_raw = QRadioButtonCustom('Raw', 1, self)
        self.rd_quality_full = QRadioButtonCustom('Full', 2, self)
        self.rd_quality_regular = QRadioButtonCustom('Regular', 3, self)
        self.rd_quality_small = QRadioButtonCustom('Small', 4, self)
        self.rd_quality_thumnail = QRadioButtonCustom('Thumnail', 5, self)
        self.radio_group_box_quality.addRadioButtonCustom(self.rd_quality_raw)
        self.radio_group_box_quality.addRadioButtonCustom(self.rd_quality_full)
        self.radio_group_box_quality.addRadioButtonCustom(self.rd_quality_regular)
        self.radio_group_box_quality.addRadioButtonCustom(self.rd_quality_small)
        self.radio_group_box_quality.addRadioButtonCustom(self.rd_quality_thumnail)
        self.grid_layout.addWidget(self.radio_group_box_quality,4,0,1,3)

        self.rd_group_box_order_by = QHRadioGroupBox('Order by',parent=self)
        self.rd_latest = QRadioButtonCustom('Latest', 1, self.rd_group_box_order_by)
        self.rd_oldest = QRadioButtonCustom('Oldest', 2, self.rd_group_box_order_by)
        self.rd_popular = QRadioButtonCustom('Popular', 3, self.rd_group_box_order_by)
        self.rd_group_box_order_by.addRadioButtonCustom(self.rd_latest)
        self.rd_group_box_order_by.addRadioButtonCustom(self.rd_oldest)
        self.rd_group_box_order_by.addRadioButtonCustom(self.rd_popular)
        self.grid_layout.addWidget(self.rd_group_box_order_by,5,0,1,3)


        self.checkbox_random = QCheckBox('Random')
        self.checkbox_random.setToolTip('Get random images, maximum is 20 images')
        self.checkbox_random.stateChanged.connect(self.randomIsTrue)
        self.grid_layout.addWidget(self.checkbox_random,6,0)

        self.btt_start = QPushButton('Start')
        self.btt_start.clicked.connect(self.download)
        self.grid_layout.addWidget(self.btt_start,7,0,1,3)
        
        self.show()

    def download(self):
        # get info download
        pass

    def randomIsTrue(self,state):
        if state > 0:
            self.rd_group_box_order_by.setEnabled(False)
            self.line_per_page.setEnabled(False)
            self.line_page.setEnabled(False)
        else:
            self.rd_group_box_order_by.setEnabled(True)
            self.line_per_page.setEnabled(True)
            self.line_page.setEnabled(True)

    def browse(self):
        file = QFileDialog.getExistingDirectory(self,"Select a folder")
        self.line_save_at.setText(file)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    app = App()
    sys.exit(a.exec_())
