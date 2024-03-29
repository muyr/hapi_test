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


class MParameterIntegerChoice(MParameterWidget):
    signal_integer_choice_parm_update = Signal(int)

    def __init__(self, parm_id, parm_label, choice_label_list, current_choice, parent=None):
        super(MParameterIntegerChoice, self).__init__(parm_id, parent)
        self.combo_box = MComboBox().small()
        self.combo_box.addItems(map(str, choice_label_list))
        self.combo_box.setCurrentIndex(current_choice)
        self.combo_box.currentIndexChanged.connect(self.slot_current_index_changed)
        self.label = MLabel(parm_label)
        self.label.setAlignment(MParameterWidget.LABEL_ALIGN)
        self.main_lay = QGridLayout()
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.setAlignment(Qt.AlignTop)
        self.main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE)
        self.main_lay.addWidget(self.label, 0, 0)
        self.main_lay.addWidget(self.combo_box, 0, 1)
        self.setLayout(self.main_lay)

    def set_help_tool_tip(self, help_str):
        if self.combo_box:
            self.combo_box.setToolTip(help_str)

    def slot_current_index_changed(self, index):
        self.signal_integer_choice_parm_update.emit(index)
