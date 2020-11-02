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

class MParameterFolderList(MParameterWidget):

    def __init__(self, parm_id, parent=None):
        super(MParameterFolderList, self).__init__(parm_id, parent)
        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        self.folder_container = MTabWidget()

        main_lay.setAlignment(Qt.AlignTop)
        main_lay.addWidget(self.folder_container)

        self.setLayout(main_lay)
        self.folder_list = []

        # self.folder_container.hide()

    def append_folder(self, folder):
        self.folder_list.append(folder)
        self.folder_container.addTab(folder, folder.get_name())
        # self.folder_container.show()
