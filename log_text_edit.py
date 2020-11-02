#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2020.1
# Email : muyanru345@163.com
###################################################################
import datetime

from dayu_widgets import *


class MLogTextEdit(MTextEdit):
    def __init__(self, parent=None):
        super(MLogTextEdit, self).__init__(parent)
        self.timestamp = False
        self.ensureCursorVisible()

    def enable_timestamp(self):
        self.timestamp = True

    def _get_now(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ') if self.timestamp else ''

    def _get_tab(self, num=0):
        return '&nbsp;&nbsp;&nbsp;&nbsp;' * num

    def _append_html(self, color, content, tab):
        self.append(
            u'<span style="color:{}">{}{}{}</span>'.format(color,
                                                           self._get_now(),
                                                           self._get_tab(tab),
                                                           content))

    def log(self, content, tab=0):
        self._append_html(dayu_theme.secondary_text_color, content, tab)

    def info(self, content, tab=0):
        self._append_html(dayu_theme.info_7, content, tab)

    def error(self, content, tab=0):
        self._append_html(dayu_theme.error_7, content, tab)

    def warning(self, content, tab=0):
        self._append_html(dayu_theme.warning_7, content, tab)

    def success(self, content, tab=0):
        self._append_html(dayu_theme.success_7, content, tab)

    def divider(self, content=None):
        if content:
            self.append('=' * 5 + content + '=' * 5)
        else:
            self.append('=' * 20)


if __name__ == '__main__':

    import sys
    from dayu_widgets.qt import *

    app = QApplication(sys.argv)
    test = MLogTextEdit()
    test.setText('<a href="www.baidu.com">baidu</a>')
    test.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
    test.show()
    sys.exit(app.exec_())
