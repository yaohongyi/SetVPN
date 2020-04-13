#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import base64
import re
from PyQt5 import QtGui, QtWidgets, QtCore
from icon import img
from public_method import SetNetwork, RestoreNetwork


with open('tmp.ico', 'wb') as tmp:
    tmp.write(base64.b64decode(img))


class Client(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 窗口绘制
        self.setFixedSize(350, 300)
        self.setWindowIcon(QtGui.QIcon('tmp.ico'))
        self.setWindowTitle('网络切换工具20200413')
        os.remove('tmp.ico')
        # 绿色上网
        self.set_button = QtWidgets.QPushButton('绿色上网(F10)')
        self.set_button.setShortcut('F10')
        self.set_button.clicked.connect(self.set_network)
        # 还原网络
        self.choose_network = QtWidgets.QLabel('请先选择联网网卡：')
        self.choose_network.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        network_info = os.popen("ipconfig /all").read()
        network_names = re.findall('.*适配器 (.*):', network_info)
        self.network_combo_box = QtWidgets.QComboBox()
        self.network_combo_box.addItems(network_names)
        self.restore_button = QtWidgets.QPushButton('还原网络(F11)')
        self.restore_button.setShortcut('F11')
        self.restore_button.clicked.connect(self.restore_network)
        # 过程打印
        self.log_browser = QtWidgets.QTextBrowser()
        # 创建窗口布局
        self.client_grid = QtWidgets.QGridLayout(self)
        self.client_grid.addWidget(self.choose_network, 0, 1, 1, 1)
        self.client_grid.addWidget(self.network_combo_box, 0, 2, 1, 1)
        self.client_grid.addWidget(self.set_button, 1, 1, 1, 1)
        self.client_grid.addWidget(self.restore_button, 1, 2, 1, 1)
        self.client_grid.addWidget(self.log_browser, 2, 1, 2, 2)

    def get_network_name(self):
        network_name = self.network_combo_box.currentText()
        return network_name

    def set_network(self):
        self.log_browser.clear()
        network_name = self.get_network_name()
        self.set_network_thread = SetNetwork(network_name)
        self.set_network_thread.text.connect(self.print_log)
        self.set_network_thread.start()

    def restore_network(self):
        self.log_browser.clear()
        network_name = self.get_network_name()
        self.restore_network_thread = RestoreNetwork(network_name)
        self.restore_network_thread.text.connect(self.print_log)
        self.restore_network_thread.start()

    def print_log(self, text):
        self.log_browser.append(text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
