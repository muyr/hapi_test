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

class MParameterString(MParameterWidget):
    signal_string_parm_update = Signal(list)

    def __init__(self, parm_id, parm_label, value_list, parent=None):
        super(MParameterString, self).__init__(parm_id, parent)

        self.main_lay = QGridLayout()
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.setAlignment(Qt.AlignTop)
        self.main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE)
        self.label = MLabel(parm_label)
        self.label.setAlignment(MParameterWidget.LABEL_ALIGN)
        self.main_lay.addWidget(self.label, 0, 0)
        self.widget_list = []
        for i, value in enumerate(value_list):
            line_edit = MLineEdit(value).small()
            line_edit.editingFinished.connect(self.slot_editing_finished)
            self.main_lay.addWidget(line_edit, 0, i + 1)
            self.widget_list.append(line_edit)
        self.setLayout(self.main_lay)

    def set_help_tool_tip(self, help_str):
        for widget in self.widget_list:
            widget.setToolTip(help_str)

    def slot_editing_finished(self):
        self.signal_string_parm_update([widget.text() for widget in self.widget_list])
