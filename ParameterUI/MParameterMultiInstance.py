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

class MParameterMultiInstance(MParameterWidget):
    def __init__(self, parm_id, parent_parm_id, parent=None):
        super(MParameterMultiInstance, self).__init__(parm_id, parent)
        self.parent_id = parent_parm_id

        self.main_lay = QGridLayout()
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        AddBefore = MPushButton("+")
        Remove = MPushButton("X")

        # AddBefore.setMaximumWidth(MultiInstanceMaxButtonWidth)
        # Remove.setMaximumWidth(MultiInstanceMaxButtonWidth)

        self.main_lay.addWidget(AddBefore, 0, 0, Qt.AlignLeft)
        self.main_lay.setColumnStretch(0, 0)
        self.main_lay.addWidget(Remove, 0, 1, Qt.AlignLeft)
        self.main_lay.setColumnStretch(1, 0)

        self.setLayout(self.main_lay)
        self.parameter_widget_list = []

    def add_parameter(self, widget):
        self.parameter_widget_list.append(widget)

        if len(self.parameter_widget_list)== 1:
            self.main_lay.addWidget(widget, len(self.parameter_widget_list) - 1, 2, 1, 1)
        else:
            self.main_lay.addWidget(widget, len(self.parameter_widget_list) - 1, 0, 1, 3)
