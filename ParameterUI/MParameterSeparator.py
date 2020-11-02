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


class MParameterSeparator(MParameterWidget):

    def __init__(self, parm_id, parent=None):
        super(MParameterSeparator, self).__init__(parm_id, parent)
        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 10, 0, 10)
        self.divider = MDivider()
        main_lay.addWidget(self.divider)
        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        if self.divider:
            self.divider.setToolTip(help_str)

