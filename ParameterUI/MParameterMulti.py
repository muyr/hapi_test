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

class MParameterMulti(MParameterWidget):
    def __init__(self, parm_id, label, instance_count, parent=None):
        super(MParameterMulti, self).__init__(parm_id, parent)
        self.num_of_instances = instance_count
        self.instance_list = []

        control_widget = QWidget()
        control_layout = QHBoxLayout()
        parameter_label = MLabel(label)

        count_line_edit = MLineEdit().small()
        count_line_edit.setText(str(self.num_of_instances))
        count_line_edit.returnPressed.connect(self.slot_instance_count_changed)

        clear_button = MPushButton("Clear").small()
        add_button = MPushButton("+").small()
        remove_button = MPushButton("-").small()

        add_button.clicked.connect(self.slot_add_instance)
        remove_button.clicked.connect(self.slot_remove_instance)
        clear_button.clicked.connect(self.slot_clear)

        control_layout.addWidget(parameter_label)
        control_layout.addWidget(count_line_edit)
        control_layout.addWidget(add_button)
        control_layout.addWidget(remove_button)
        control_layout.addWidget(clear_button)

        control_widget.setLayout(control_layout)

        self.main_lay = QVBoxLayout()
        # self.main_lay.setAlignment(Qt.AlignTop)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.main_lay.addWidget(control_widget)
        self.setLayout(self.main_lay)


    def append_instance(self, Instance):
        self.instance_list.append(Instance)
        self.main_lay.addWidget(Instance)

    def get_instance(self, index):
        if index < len(self.instance_list):
            return self.instance_list[index]
        else:
            return None

    def slot_instance_count_changed(self):
        pass

    def slot_add_instance(self):
        pass

    def slot_remove_instance(self):
        pass

    def slot_clear(self):
        pass
