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

class MParameterToggle(MParameterWidget):
    signal_toggle_parm_update = Signal(list)

    def __init__(self, parm_id, parm_label, checked, parent=None):
        super(MParameterToggle, self).__init__(parm_id, parent)
        self.toggle = MCheckBox(text=parm_label)
        self.toggle.setChecked(checked)
        self.toggle.stateChanged.connect(self.slot_state_changed)

        main_lay = QGridLayout()
        main_lay.setAlignment(Qt.AlignTop)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE+6)
        # main_lay.addWidget(MLabel(), 0, 0)
        main_lay.addWidget(self.toggle, 0, 1)
        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        if self.toggle:
            self.toggle.setToolTip(help_str)

    def slot_state_changed(self, state):
        self.signal_toggle_parm_update.emit(1 if self.toggle.isChecked() else 0)
