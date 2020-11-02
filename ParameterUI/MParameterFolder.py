#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from MParameterWidget import MParameterWidget
from dayu_widgets.qt import *
from dayu_widgets import *

class MParameterFolder(MParameterWidget):

    def __init__(self, parm_id, folder_name, parent=None):
        super(MParameterFolder, self).__init__(parm_id, parent)
        self.row_count = 0
        self.parameter_widget_list = []
        self.name = folder_name
        self.row_lay_list = []

        self.main_lay = QGridLayout()
        self.main_lay.setAlignment(Qt.AlignTop)

        self.setLayout(self.main_lay)

    def append_new_row(self, widget):
        new_row_lay = QHBoxLayout()
        new_row_lay.addWidget(widget)
        self.main_lay.addLayout(new_row_lay, self.row_count, 0)
        self.parameter_widget_list.append(widget)
        self.row_lay_list.append(new_row_lay)
        self.row_count += 1

    def add_widget_to_row(self, widget, row):
        if row < self.row_count:
            self.parameter_widget_list.append(widget)
            self.row_lay_list[row].addWidget(widget)

    def get_name(self):
        return self.name
