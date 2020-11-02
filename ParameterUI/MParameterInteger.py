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

class MParameterInteger(MParameterWidget):
    signal_integer_parm_update = Signal(list)

    def __init__(self, parm_id, pram_label, value_list, ui_min, ui_max, parent=None):
        super(MParameterInteger, self).__init__(parm_id, parent)
        main_lay = QGridLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        self.label = MLabel(pram_label)
        self.label.setAlignment(MParameterWidget.LABEL_ALIGN)
        main_lay.addWidget(self.label, 0, 0)
        self.widget_list = []
        for i, value in enumerate(value_list):
            line_edit = MLineEdit(str(value)).small()
            line_edit.editingFinished.connect(self.slot_editing_finished)
            main_lay.addWidget(line_edit, 0, i + 1)
            self.widget_list.append(line_edit)

        self.slider = None
        self.ui_min = ui_min
        self.ui_max = ui_max
        if len(value_list) == 1:
            self.slider = MSlider(Qt.Horizontal)
            self.slider.disable_show_text()
            self.slider.setRange(self.ui_min, self.ui_max)
            self.slider.setSingleStep(1)
            self.slider.setPageStep(1)
            main_lay.addWidget(self.slider, 0, 2)

            self.update_slider_position()
            self.slider.valueChanged.connect(self.slot_slider_value_changed)
            self.slider.sliderReleased.connect(self.slot_slider_released)

            main_lay.setColumnStretch(1, 30)
            main_lay.setColumnStretch(2, 70)
        main_lay.setAlignment(Qt.AlignTop)
        main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE)

        self.setLayout(main_lay)

    def set_help_tool_tip(self, help_str):
        for widget in self.widget_list:
            widget.setToolTip(help_str)
        if self.slider:
            self.slider.setToolTip(help_str)

    def calculate_slider_position(self):
        return int(self.widget_list[0].text())

    def update_slider_position(self):
        if self.slider:
            self.slider.setSliderPosition(self.calculate_slider_position())

    def calculate_value_from_slider_position(self):
        return self.slider.sliderPosition()

    def get_integer_values(self):
        return [int(widget.text()) for widget in self.widget_list]

    def slot_editing_finished(self):
        self.signal_integer_parm_update.emit(self.get_integer_values())

    def slot_slider_value_changed(self, value):
        self.widget_list[0].setText(str(value))

    def slot_slider_released(self):
        self.widget_list[0].setText(str(self.calculate_value_from_slider_position()))
        self.signal_integer_parm_update.emit(self.get_integer_values())
