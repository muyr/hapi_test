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
import os

class MParameterNode(MParameterWidget):
    signal_path_file_parm_update = Signal(str)

    def __init__(self, parm_id, parm_label, node_name, parent=None):
        super(MParameterNode, self).__init__(parm_id, parent)
        self.line_edit = MLineEdit().small()
        self.line_edit.editingFinished.connect(self.slot_path_file_changed)
        self.button = MClickBrowserFileToolButton()
        self.button.sig_file_changed.connect(self.line_edit.setText)
        if node_name:
            self.line_edit.setText(node_name)
            self.button.set_dayu_path(os.path.dirname(node_name))
        self.label = MLabel(parm_label)
        self.label.setAlignment(MParameterWidget.LABEL_ALIGN)
        main_lay = QGridLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setAlignment(Qt.AlignTop)
        main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE)
        main_lay.addWidget(self.label, 0, 0)
        main_lay.addWidget(self.line_edit, 0, 1)
        main_lay.addWidget(self.button, 0, 2)
        main_lay.setColumnStretch(1, 100)
        main_lay.setColumnStretch(2, 0)
        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        if self.line_edit:
            self.line_edit.setToolTip(help_str)

    def slot_path_file_changed(self):
        self.signal_path_file_parm_update.emit(self.line_edit.text())
