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


class MParameterLabel(MParameterWidget):

    def __init__(self, parm_id, label_text, parent=None):
        super(MParameterLabel, self).__init__(parm_id, parent)
        self.label = MLabel(label_text)

        main_lay = QGridLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setAlignment(Qt.AlignLeft)
        main_lay.addWidget(self.label)
        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        if self.label:
            self.label.setToolTip(help_str)

