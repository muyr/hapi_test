#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.10
# Email : muyanru345@163.com
###################################################################

from dayu_widgets.qt import *
from dayu_widgets import *
from HAPI import MAPI
from log_text_edit import MLogTextEdit
from hdata import ParmType
from MColorWidget import MColorWidget
from MFloatWidget import MFloatWidget
from MIntWidget import MIntWidget
from MParameterViewer import MParameterViewer
import traceback
WIDGET_MAP = {
    ParmType.INT: (MIntWidget, 'setValue'),
    ParmType.FLOAT: (MFloatWidget, 'setValue'),
    ParmType.FOLDER: (MLineEdit, 'setText'),
    ParmType.TOGGLE: (MSwitch, 'setChecked'),
    ParmType.COLOR: (MColorWidget, 'setValue')
}

class MCookThread(QThread):
    def __init__(self, hapi, parent=None):
        super(MCookThread, self).__init__(parent)
        self._client = hapi._client
        self._node_id = None
        self._cook_options = hapi._cook_options

    def set_client(self, client):
        self._client = client

    def set_node_id(self, node_id):
        self._node_id = node_id

    def set_cook_options(self, cook_options):
        self._cook_options = cook_options

    def run(self):
        cook_result = self._client.CookNode(node_id=self._node_id, cook_options=self._cook_options)
        print cook_result
    #     cook_status =
    #     cook_result
    #     while True:
    #         if cookStatus > HAPI_STATE_MAX_READY_STATE and cookResult == HAPI_RESULT_SUCCESS:
    #
    #
    # int cookStatus;
    # HAPI_Result cookResult;
    # do
    # {
    #     cookResult = HAPI_GetStatus( &session, HAPI_STATUS_COOK_STATE, &cookStatus );
    # }
    # while ( cookStatus > HAPI_STATE_MAX_READY_STATE && cookResult == HAPI_RESULT_SUCCESS );
    # ENSURE_SUCCESS( cookResult );
    # ENSURE_COOK_SUCCESS( cookStatus );


class MyHoudiniEngineApp(QWidget):
    def __init__(self, parent=None):
        super(MyHoudiniEngineApp, self).__init__(parent)
        self.setWindowTitle('Houdini Engine for Messiah')
        self.setWindowIcon(QIcon('./logo.png'))
        self.host_line_edit = MLineEdit(text='localhost').small()
        self.port_spin_box = MSpinBox().small()
        self.port_spin_box.setRange(100, 9999)
        self.port_spin_box.setValue(9090)
        self.port_spin_box.setFixedWidth(100)
        self.connect_button = MPushButton(text='Start').primary().small()
        self.connect_button.clicked.connect(self.slot_connect)

        connect_lay = QHBoxLayout()
        connect_lay.addWidget(MLabel('Port:'))
        connect_lay.addWidget(self.port_spin_box)
        connect_lay.addSpacing(10)
        connect_lay.addWidget(self.connect_button)
        connect_lay.addStretch()

        self.hda_file_button = MDragFileButton(text='Drop HDA or OTL File here')
        self.hda_file_button.set_dayu_multiple(False)
        self.hda_file_button.set_dayu_filters(['.hda', '.otl'])
        self.hda_file_button.set_dayu_path(r'D:\mu_data\hda')
        self.hda_file_label = MLabel().secondary()
        self.hda_file_label.setAlignment(Qt.AlignCenter)

        self.hda_file_button.sig_file_changed.connect(self.slot_hda_file)

        self._cook_button = MPushButton(text='Cook').primary()
        self._cook_button.clicked.connect(self.slot_cook)
        self._save_hip_button = MPushButton(text='Save HIP')
        self._save_hip_button.clicked.connect(self.slot_save_hip)
        button_lay = QHBoxLayout()
        button_lay.addWidget(self._cook_button)
        button_lay.addWidget(self._save_hip_button)

        self.parm_viewer = MParameterViewer()
        left_widget = QWidget()
        left_lay = QVBoxLayout()
        left_widget.setLayout(left_lay)
        left_lay.addWidget(MDivider('Parameters'))
        left_lay.addWidget(self.parm_viewer)
        left_lay.setStretchFactor(self.parm_viewer, 100)

        self.log_text_edit = MLogTextEdit()
        self.log_text_edit.enable_timestamp()
        right_widget = QWidget()
        right_lay = QVBoxLayout()
        right_widget.setLayout(right_lay)
        right_lay.addLayout(connect_lay)
        right_lay.addWidget(MDivider('HDA/OTL File Reader'))
        right_lay.addWidget(self.hda_file_button)
        right_lay.addWidget(self.hda_file_label)
        right_lay.addWidget(MDivider('Operator'))
        right_lay.addLayout(button_lay)
        right_lay.addWidget(MDivider('Log Information'))
        right_lay.addWidget(self.log_text_edit)
        right_lay.setStretchFactor(self.log_text_edit, 100)

        splitter = QSplitter()
        splitter.addWidget(right_widget)
        splitter.addWidget(left_widget)
        splitter.setStretchFactor(0, 40)
        splitter.setStretchFactor(1, 60)

        main_lay = QVBoxLayout()
        self.setLayout(main_lay)
        main_lay.addWidget(splitter)

        geo = QApplication.desktop().screenGeometry()
        self.setGeometry(geo.width() / 4, geo.height() / 4, geo.width()/2, geo.height()/2)

        self.cook_thread = None
        self.node_id = None
        self.hapi = None

    def slot_connect(self):
        if self.connect_button.text() == 'Start':
            try:
                self.hapi = MAPI(port=str(self.port_spin_box.value()))
                self.hapi.init()
                self.cook_thread = MCookThread(self.hapi)
                self.log_text_edit.success('Connect success.')
                self.connect_button.setText('Stop')
                MMessage.success(text='Connect success', parent=self)
            except Exception as e:
                self.log_text_edit.error(str(e))
                MMessage.error(text='Connect Failed', parent=self)
        else:
            try:
                self.hapi.disconnect()
                self.connect_button.setText('Start')
                self.log_text_edit.success('Disconnect success.')
                MMessage.success(text='Disconnect success', parent=self)
            except Exception as e:
                self.log_text_edit.error(str(e))
                MMessage.error(text='Disconnect Failed', parent=self)

    def slot_hda_file(self, hda_file):
        self.hda_file_label.setText(hda_file)
        if self.hapi is None:
            self.slot_connect()
        self.hapi._client.Cleanup()
        self.hapi.init()
        try:
            self.log_text_edit.log(u'Begin Load "{}"'.format(hda_file))
            hda_name = self.hapi.load_hda(hda_file)
            self.log_text_edit.success(u'Load "{}" success'.format(hda_name))
            instance_result = self.hapi.instance_hda(hda_name)
            self.node_id = instance_result.new_node_id
            self.log_text_edit.success(u'Instance "{}" success'.format(hda_name))
            asset_info =  self.hapi.get_asset_info(self.node_id)
            self.parm_viewer.set_node(asset_info.nodeId)
            self.parm_viewer.set_client(self.hapi)
            self.parm_viewer.refresh()
        except Exception as e:
            self.log_text_edit.append(str(traceback.print_exc()))

    def slot_cook(self):
        # self.hapi._client.SetParmIntValue(self.node_id, 'randomseed', 0, 22)
        # self.hapi._client.Cook()
        self.hapi.cook(node_id=self.node_id)

    def slot_save_hip(self):
        hip_file, _ = QFileDialog.getSaveFileName(self, 'Save As...', 'test', 'HIP(*.hip)')
        result = self.hapi.save_to_hip(hip_file)
        if result == 0:
            MMessage.success(parent=self, text='Save success!')
            self.log_text_edit.success(u'Save to {}'.format(hip_file))

    def closeEvent(self, *args, **kwargs):
        if self.hapi:
            self.hapi.disconnect()
        return super(MyHoudiniEngineApp, self).closeEvent(*args, **kwargs)

if __name__ == '__main__':

    import sys
    from dayu_widgets import dayu_theme

    app = QApplication(sys.argv)
    test = MyHoudiniEngineApp()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
