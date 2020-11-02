#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from dayu_widgets.qt import *



class MParameterWidget(QWidget):
    LABEL_SPAN_VALUE = 140
    LABEL_ALIGN = Qt.AlignLeft
    def __init__(self, parm_id, parent=None):
        super(MParameterWidget, self).__init__(parent)
        self._id = parm_id

    def set_help_tool_tip(self, help_str):
        self.setToolTip(help_str)
