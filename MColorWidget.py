#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from dayu_widgets.qt import *
from dayu_widgets import *


class MColorWidget(QWidget):
    def __init__(self, parent=None):
        super(MColorWidget, self).__init__(parent)
        self.choose_color_button = QPushButton()
        self.choose_color_button.setFixedSize(QSize(70, 24))
        self.choose_color_button.clicked.connect(self.slot_change_color)
        self.r_spin_box = MDoubleSpinBox().small()
        self.g_spin_box = MDoubleSpinBox().small()
        self.b_spin_box = MDoubleSpinBox().small()
        self.r_spin_box.setDecimals(10)
        self.g_spin_box.setDecimals(10)
        self.b_spin_box.setDecimals(10)
        main_lay = QHBoxLayout()
        self.setLayout(main_lay)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.addWidget(self.choose_color_button)
        main_lay.addWidget(self.r_spin_box)
        main_lay.addWidget(self.g_spin_box)
        main_lay.addWidget(self.b_spin_box)

    def slot_change_color(self):
        dialog = QColorDialog(parent=self)
        dialog.currentColorChanged.connect(self.slot_color_changed)
        dialog.show()

    def slot_color_changed(self, color):
        self.r_spin_box.setValue(color.redF())
        self.g_spin_box.setValue(color.greenF())
        self.b_spin_box.setValue(color.blueF())
        self.choose_color_button.setStyleSheet('border-radius: 0;border: none;border:2px solid gray;'
                                               'background-color:{};'.format(color.name()))

    def setValue(self, value):
        color = QColor()
        color.setRedF(value[0])
        color.setGreenF(value[1])
        color.setBlueF(value[2])
        self.slot_color_changed(color)
        # self.r_spin_box.setValue(value[0])
        # self.g_spin_box.setValue(value[1])
        # self.b_spin_box.setValue(value[2])

    def setMaximum(self, value):
        self.r_spin_box.setMaximum(value)
        self.g_spin_box.setMaximum(value)
        self.b_spin_box.setMaximum(value)

    def setMinimum(self,value):
        self.r_spin_box.setMinimum(value)
        self.g_spin_box.setMinimum(value)
        self.b_spin_box.setMinimum(value)

if __name__ == '__main__':

   import sys

   app = QApplication(sys.argv)
   test = MColorWidget()
   test.show()
   sys.exit(app.exec_())
