#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from MParameterWidget import MParameterWidget
from dayu_widgets import *
from dayu_widgets.qt import *


class MParameterButton(MParameterWidget):
    signal_button_parm_update = Signal()

    def __init__(self, parm_id, parm_label, parent=None):
        super(MParameterButton, self).__init__(parm_id, parent)
        self.button = MPushButton(parm_label).small()
        self.button.clicked.connect(self.signal_button_parm_update)

        main_lay = QGridLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setAlignment(Qt.AlignTop)
        main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE + 6)
        main_lay.addWidget(self.button, 0, 1)

        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        if self.button:
            self.button.setToolTip(help_str)
