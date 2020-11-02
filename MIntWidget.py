#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from dayu_widgets.qt import *
from dayu_widgets import *


class MIntWidget(QWidget):
    def __init__(self, parent=None):
        super(MIntWidget, self).__init__(parent)
        self.spin_box = MSpinBox().small()
        self.spin_box.setFixedWidth(100)
        self.slider = MSlider()
        self.spin_box.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.spin_box.setValue)

        main_lay = QHBoxLayout()
        self.setLayout(main_lay)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(self.spin_box)
        main_lay.addWidget(self.slider)

    def setValue(self, value):
        self.spin_box.setValue(value)
        self.slider.setValue(value)

    def setMaximum(self, value):
        self.spin_box.setMaximum(value)
        self.slider.setMaximum(value)

    def setMinimum(self,value):
        self.spin_box.setMinimum(value)
        self.slider.setMinimum(value)

    # def setToolTip(self, text):
    #     self.spin_box.setToolTip(text)

if __name__ == '__main__':

   import sys

   app = QApplication(sys.argv)
   test = MIntWidget()
   test.show()
   sys.exit(app.exec_())
