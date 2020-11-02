#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################
from ParameterUI import *
from dayu_widgets.qt import *
from dayu_widgets import *
from hdata import ParmType
from HAPI import MAPI
import functools


class MParameterViewer(QWidget):
    def __init__(self, parent=None):
        super(MParameterViewer, self).__init__(parent)
        self.asset_name_label = MLabel().strong().mark()
        self.refresh_button = MToolButton().icon_only().svg('refresh_line.svg')
        self.refresh_button.clicked.connect(self.refresh)
        title_lay = QHBoxLayout()
        title_lay.addWidget(self.refresh_button)
        title_lay.addWidget(self.asset_name_label)
        # title_lay.addStretch()
        self.parameters_detail_grid_layout = QGridLayout()
        self.parameters_detail_grid_layout.setContentsMargins(0, 0, 5, 0)
        self.parameters_detail_grid_layout.setAlignment(Qt.AlignTop)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.parameters_detail_grid_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_lay)
        main_layout.addWidget(scroll_area)

        # Setup UI
        self.setLayout(main_layout)

        # Internal
        self.row_count = 0
        self.node_id = -1
        self.widget_list = []
        self.parameters_detail_rows = []

    def set_client(self, client):
        self.hapi = client

    def set_node(self, node_id):
        self.node_id = node_id

    def clear_node(self):
        self.node_id = -1

    def _clear(self):
        # Clear any existing widgets
        for widget in self.widget_list:
            if widget:
                widget.deleteLater()
        self.widget_list = []

    def refresh(self):
        self._clear()

        node_info = self.hapi._client.GetNodeInfo(self.node_id).node_info
        param_list = self.hapi._client.GetParameters(self.node_id, 0,
                                                     node_info.parmCount).parm_infos_array
        self.asset_name_label.setText(self.hapi.get_string(node_info.nameSH))
        multi_list_cache = {}
        folder_cache = {}
        parsing_folder_list = False
        active_folder_list = None  # MParameterFolderList
        remaining_folders = 0
        widget_to_add = None  # ParameterWidget
        for parm_info in param_list:
            label_str = self.hapi.get_string(parm_info.labelSH)
            help_str = self.hapi.get_string(parm_info.helpSH)
            if parm_info.type == ParmType.FOLDERLIST:
                widget_to_add = self.create_folder_list_widget(parm_info)
                if parm_info.size > 0:
                    parsing_folder_list = True
                    remaining_folders = parm_info.size
                    active_folder_list = widget_to_add
            if parm_info.type == ParmType.FOLDER:
                widget_to_add = self.create_folder_widget(parm_info)
                folder_cache.update({parm_info.id: widget_to_add})
            if parm_info.type == ParmType.LABEL:
                widget_to_add = self.create_label_widget(parm_info)
            if parm_info.type == ParmType.INT:
                if parm_info.choiceCount > 0:
                    widget_to_add = self.create_integer_choice_widget(parm_info)
                else:
                    widget_to_add = self.create_integer_widget(parm_info)
            if parm_info.type == ParmType.FLOAT:
                widget_to_add = self.create_float_widget(parm_info)
            if parm_info.type == ParmType.COLOR:
                color = self.hapi._client.GetParmFloatValues(node_id=self.node_id,
                                                             start=parm_info.floatValuesIndex,
                                                             length=parm_info.size).values_array
                widget_to_add = MParameterColor(parm_info.id, label_str, color=color)
                widget_to_add.signal_color_parm_update.connect(functools.partial(self.slot_float_parm_update, parm_info))
            if parm_info.type == ParmType.STRING:
                if parm_info.choiceCount > 0:
                    widget_to_add = self.create_string_choice_widget(parm_info)
                else:
                    widget_to_add = self.create_string_widget(parm_info)
            if parm_info.type == ParmType.TOGGLE:
                widget_to_add = self.create_toggle_widget(parm_info)
            if parm_info.type == ParmType.BUTTON:
                widget_to_add = self.create_button_widget(parm_info)
            if parm_info.type == ParmType.SEPARATOR:
                widget_to_add = MParameterSeparator(parm_info.id)
            if parm_info.type == ParmType.MULTIPARMLIST:
                print label_str, '\tmultilist'
                widget_to_add = self.create_multi_widget(parm_info)
                multi_list_cache.update({parm_info.id: widget_to_add})
            if parm_info.type == ParmType.NODE:
                value_result = self.hapi._client.GetParmStringValues(node_id=self.node_id,
                                                                     evaluate=False,
                                                                     start=parm_info.stringValuesIndex,
                                                                     length=parm_info.size).values_array
                value_result = map(self.hapi.get_string, value_result)
                widget_to_add = MParameterNode(parm_id=parm_info.id, parm_label=label_str,
                                               node_name=value_result[0])
                widget_to_add.signal_path_file_parm_update.connect(
                    functools.partial(self.slot_string_parm_update, parm_info))

            if parm_info.type == ParmType.PATH_FILE:
                value_result = self.hapi._client.GetParmStringValues(node_id=self.node_id,
                                                                     evaluate=False,
                                                                     start=parm_info.stringValuesIndex,
                                                                     length=parm_info.size).values_array
                value_result = map(self.hapi.get_string, value_result)
                widget_to_add = MParameterPathFile(parm_id=parm_info.id, parm_label=label_str,
                                                   path_file=value_result[0])
                widget_to_add.signal_path_file_parm_update.connect(
                    functools.partial(self.slot_string_parm_update, parm_info))

            if parm_info.type == ParmType.PATH_FILE_DIR:
                print label_str, '\tpath_file_dir'
            if parm_info.type == ParmType.PATH_FILE_GEO:
                print label_str, '\tpath_file_geo'
            if parm_info.type == ParmType.PATH_FILE_IMAGE:
                print label_str, '\tpath_file_image'
            if widget_to_add:
                if parsing_folder_list and parm_info.type != ParmType.FOLDERLIST:
                    folder = widget_to_add
                    if not parm_info.invisible:
                        active_folder_list.append_folder(folder)
                    remaining_folders -= 1

                    if remaining_folders <= 0:
                        parsing_folder_list = False
                elif self.is_parameter_root_level(parm_info):
                    self.append_new_row(widget_to_add)
                elif parm_info.isChildOfMultiParm:
                    search = multi_list_cache.get(parm_info.parentId, None)
                    if search:
                        multi_parm = search
                        instance = multi_parm.get_instance(self.get_multi_parm_index(parm_info))

                        if (instance):
                            instance.AddParameter(widget_to_add)
                        else:
                            new_instance = MParameterMultiInstance(parm_info.id, parm_info.parentId)
                            new_instance.add_parameter(widget_to_add)
                            multi_parm.append_instance(new_instance)

                else:
                    folder_search = folder_cache.get(parm_info.parentId, None)
                    if folder_search:
                        folder = folder_search
                        folder.append_new_row(widget_to_add)

                if parm_info.invisible:
                    widget_to_add.hide()

                if parm_info.disabled:
                    widget_to_add.setEnabled(False)

                if help_str and not help_str.startswith('Null string'):
                    widget_to_add.set_help_tool_tip(help_str)

    def is_parameter_root_level(self, parm_info):
        return parm_info.parentId < 0

    def get_multi_parm_index(self, parm_info):
        instance_num = parm_info.instanceNum
        return instance_num - 1 if parm_info.instanceStartOffset else instance_num

    def append_new_row(self, widget):
        self.widget_list.append(widget)
        new_row = QHBoxLayout()
        self.parameters_detail_rows.append(new_row)
        self.parameters_detail_grid_layout.addLayout(new_row, self.row_count, 0)
        new_row.addWidget(widget)

        self.row_count += 1

    def add_widget_to_row(self, widget, row):
        if row < self.row_count:
            self.widget_list.append(widget)
            self.parameters_detail_rows[row].addWidget(widget)

    def create_folder_widget(self, parm_info):
        return MParameterFolder(parm_info.id, self.hapi.get_string(parm_info.labelSH))

    def create_folder_list_widget(self, parm_info):
        return MParameterFolderList(parm_info.id)

    def create_label_widget(self, parm_info):
        return MParameterLabel(parm_info.id, self.hapi.get_string(parm_info.labelSH))

    def create_integer_widget(self, parm_info):
        value_result = self.hapi._client.GetParmIntValues(node_id=self.node_id,
                                                          start=parm_info.intValuesIndex,
                                                          length=parm_info.size).values_array
        widget = MParameterInteger(parm_info.id,
                                   self.hapi.get_string(parm_info.labelSH),
                                   value_result,
                                   parm_info.UIMin, parm_info.UIMax)
        widget.signal_integer_parm_update.connect(
            functools.partial(self.slot_integer_parm_update, parm_info))
        return widget

    def create_float_widget(self, parm_info):
        value_result = self.hapi._client.GetParmFloatValues(node_id=self.node_id,
                                                            start=parm_info.floatValuesIndex,
                                                            length=parm_info.size).values_array
        widget = MParameterFloat(parm_info.id,
                                 self.hapi.get_string(parm_info.labelSH),
                                 value_result,
                                 parm_info.UIMin,
                                 parm_info.UIMax)
        widget.signal_float_parm_update.connect(
            functools.partial(self.slot_float_parm_update, parm_info))
        return widget

    def create_string_widget(self, parm_info):
        value_result = self.hapi._client.GetParmStringValues(node_id=self.node_id,
                                                             evaluate=True,
                                                             start=parm_info.stringValuesIndex,
                                                             length=parm_info.size).values_array
        value_result = map(self.hapi.get_string, value_result)
        widget = MParameterString(parm_info.id,
                                  self.hapi.get_string(parm_info.labelSH),
                                  value_result)
        widget.signal_string_parm_update.connect(
            functools.partial(self.slot_string_parm_update, parm_info))
        return widget

    def create_toggle_widget(self, parm_info):
        value_result = self.hapi._client.GetParmIntValues(node_id=self.node_id,
                                                          start=parm_info.intValuesIndex,
                                                          length=parm_info.size).values_array
        widget = MParameterToggle(parm_info.id,
                                  self.hapi.get_string(parm_info.labelSH),
                                  value_result[0])
        widget.signal_toggle_parm_update.connect(
            functools.partial(self.slot_integer_parm_update, parm_info))
        return widget

    def create_button_widget(self, parm_info):
        widget = MParameterButton(parm_info.id, self.hapi.get_string(parm_info.labelSH))
        widget.signal_button_parm_update.connect(
            functools.partial(self.slot_integer_parm_update, parm_info))
        return widget

    def create_integer_choice_widget(self, parm_info):
        choice_infos = self.hapi._client.GetParmChoiceLists(self.node_id,
                                                            parm_info.choiceIndex,
                                                            parm_info.choiceCount).parm_choices_array

        choice_labels = [self.hapi.get_string(i.labelSH) for i in choice_infos]
        current_choice = self.hapi._client.GetParmIntValues(self.node_id,
                                                            parm_info.intValuesIndex,
                                                            1).values_array
        widget = MParameterIntegerChoice(parm_id=parm_info.id,
                                         parm_label=self.hapi.get_string(parm_info.labelSH),
                                         choice_label_list=choice_labels,
                                         current_choice=current_choice[0])
        widget.signal_integer_choice_parm_update.connect(
            functools.partial(self.slot_integer_parm_update, parm_info))

        return widget

    def create_string_choice_widget(self, parm_info):
        choice_infos = self.hapi._client.GetParmChoiceLists(self.node_id,
                                                            parm_info.choiceIndex,
                                                            parm_info.choiceCount).parm_choices_array
        choice_labels = [self.hapi.get_string(i.labelSH) for i in choice_infos]
        choice_values = [self.hapi.get_string(i.valueSH) for i in choice_infos]

        current_choice = self.hapi._client.GetParmStringValues(self.node_id,
                                                               True,
                                                               parm_info.stringValuesIndex,
                                                               1).values_array
        selection = self.hapi.get_string(current_choice[0])

        widget = MParameterStringChoice(parm_id=parm_info.id,
                                        parm_label=self.hapi.get_string(parm_info.labelSH),
                                        choice_label_list=choice_labels,
                                        choice_value_list=choice_values,
                                        current_choice=selection)

        widget.signal_string_choice_parm_update.connect(
            functools.partial(self.slot_string_parm_update, parm_info))
        return widget

    def create_multi_widget(self, parm_info):
        return MParameterMulti(parm_info.id,
                               self.hapi.get_string(parm_info.labelSH),
                               parm_info.instanceCount)

    def slot_integer_parm_update(self, parm_info, value_list):
        if not isinstance(value_list, list):
            value_list = [value_list]
        for i, value in enumerate(value_list):
            self.hapi._client.SetParmIntValue(node_id=self.node_id,
                                              parm_name=self.hapi.get_string(parm_info.nameSH),
                                              index=i,
                                              value=value)
        self.refresh()

    def slot_float_parm_update(self, parm_info, value_list):
        if not isinstance(value_list, list):
            value_list = [value_list]
        for i, value in enumerate(value_list):
            self.hapi._client.SetParmFloatValue(node_id=self.node_id,
                                              parm_name=self.hapi.get_string(parm_info.nameSH),
                                              index=i,
                                              value=value)
        self.refresh()

    def slot_string_parm_update(self, parm_info, value_list):
        if not isinstance(value_list, list):
            value_list = [value_list]
        for i, value in enumerate(value_list):
            self.hapi._client.SetParmStringValue(node_id=self.node_id,
                                              parm_name=self.hapi.get_string(parm_info.nameSH),
                                              index=i,
                                              value=value)
        self.refresh()

    def slot_multi_parm_update(self):
        pass
