# Thư viện này có chứa một số class
# giúp việc tạo các widget thuận tiện và nhanh hơn#
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QRadioButton

class QRadioButtonCustom(QRadioButton):

    def __init__(self, str, value, parent=None):
        super().__init__(str, parent=parent)
        self.value = value

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value

class QHRadioGroupBox(QGroupBox):

    def __init__(self, str, *QRadioButtonCustoms, parent=None):
        '''
        Triển khai một group radio button theo chiều ngang
        :param `*QRadioButtonCustoms`: Truyền vào các QRadioButtonCustom
        '''
        super().__init__(str, parent=parent)
        self.value = ''
        self.radioButtons = QRadioButtonCustoms
        self.hbox_layout = QHBoxLayout(self)
        self.setLayout(self.hbox_layout)
        for i in self.radioButtons:
            i.toggled.connect(self.__setValue)
            self.hbox_layout.addWidget(i)

    def addRadioButtonCustom(self, radioButtonCustom):
        radioButtonCustom.toggled.connect(self.__setValue)
        self.hbox_layout.addWidget(radioButtonCustom)

    def getValue(self):
        return self.value

    def __setValue(self):
        rd = self.sender()
        if rd.isChecked():
            self.value = rd.getValue()
