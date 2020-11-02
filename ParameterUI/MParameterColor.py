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


class MParameterColor(MParameterWidget):
    signal_color_parm_update = Signal(list)

    def __init__(self, parm_id, param_label, color, parent=None):
        super(MParameterColor, self).__init__(parm_id, parent)
        self._color = color
        self.label = MLabel(param_label)
        self.label.setAlignment(MParameterWidget.LABEL_ALIGN)
        self.choose_color_button = QPushButton()
        self.choose_color_button.setFixedSize(QSize(70, 24))
        self.choose_color_button.clicked.connect(self.slot_change_color)

        main_lay = QGridLayout()
        main_lay.setAlignment(Qt.AlignTop)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.addWidget(self.label, 0, 0)
        main_lay.addWidget(self.choose_color_button, 0, 1)
        main_lay.setColumnMinimumWidth(0, MParameterWidget.LABEL_SPAN_VALUE)

        self.widget_list = []
        for i, value in enumerate(color):
            line_edit = MLineEdit().small()
            line_edit.editingFinished.connect(self.slot_edit_finished)
            line_edit.setText(str(value))
            main_lay.addWidget(line_edit, 0, i + 2)
            self.widget_list.append(line_edit)

        q_color = self._list_to_color(color)
        self.choose_color_button.setStyleSheet(
            'border-radius: 0;border: none;border:2px solid gray;'
            'background-color:{};'.format(q_color.name()))
        self.setLayout(main_lay)

    def slot_change_color(self):
        dialog = QColorDialog(parent=self)
        # dialog.setCurrentColor(self._color)
        dialog.currentColorChanged.connect(self.slot_color_changed)
        dialog.show()

    def slot_color_changed(self, color):
        color_list = self._color_to_list(color)
        for i, value in enumerate(color_list):
            self.widget_list[i].setText(str(value))
        self.choose_color_button.setStyleSheet(
            'border-radius: 0;border: none;border:2px solid gray;'
            'background-color:{};'.format(color.name()))
        self._color = color
        self.signal_color_parm_update.emit(color_list)

    def slot_edit_finished(self):
        color_list = [float(widget.text()) for widget in self.widget_list]
        color = self._list_to_color(color_list)
        self.choose_color_button.setStyleSheet(
            'border-radius: 0;border: none;border:2px solid gray;'
            'background-color:{};'.format(color.name()))
        self._color = color
        self.signal_color_parm_update(color_list)

    def _list_to_color(self, color_list):
        color = QColor()
        color.setRedF(color_list[0])
        color.setGreenF(color_list[1])
        color.setBlueF(color_list[2])
        return color

    def _color_to_list(self, color):
        return [color.redF(), color.greenF(), color.blueF()]

    def set_help_tool_tip(self, help_str):
        for widget in self.widget_list:
            widget.setToolTip(help_str)
        self.choose_color_button.setToolTip(help_str)
