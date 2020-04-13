#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import time
import os
import socket
from PyQt5 import QtCore


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class SetNetwork(QtCore.QThread):
    """设置IP、子网掩码、网关、DNS"""
    text = QtCore.pyqtSignal(str)

    def __init__(self, network_name):
        super().__init__()
        self.network_name = network_name

    def set_network(self):
        ip_address = get_host_ip()
        subnet_mask = '255.255.255.0'
        gateway = '192.168.0.150'
        dns_server = '192.168.0.38'
        # 设置IP
        set_ip_command = f"netsh interface ip set address name={self.network_name} source=static " \
            f"addr={ip_address} mask={subnet_mask} gateway={gateway}"
        os.popen(set_ip_command)
        # 设置DNS服务
        set_dns_command = f"netsh interface ip set dns name={self.network_name} source=static " \
            f"addr={dns_server} register=primary"
        os.popen(set_dns_command)
        self.text.emit('绿色上网设置成功，当前网络设置如下：')
        self.text.emit(f'IP地址 - {ip_address}')
        self.text.emit(f'子网掩码 - {subnet_mask}')
        self.text.emit(f'默认网关 - {gateway}')
        self.text.emit(f'DNS地址 - {dns_server}')
        self.text.emit('')
        time.sleep(1)
        self.text.emit("让我们开始遨游吧···")
        time.sleep(3)

    def run(self):
        self.set_network()


class RestoreNetwork(QtCore.QThread):
    """自动获取IP地址、DNS服务器地址"""
    text = QtCore.pyqtSignal(str)

    def __init__(self, network_name):
        super().__init__()
        self.network_name = network_name

    def restore_network(self):
        self.text.emit('开始设置自动获取IP和DNS，请耐心等待···')
        restore_ip_command = f'netsh interface ip set address name={self.network_name} source=dhcp'
        os.popen(restore_ip_command)
        restore_dns_command = f'netsh interface ip set dns name={self.network_name} source=dhcp'
        os.popen(restore_dns_command)
        for i in range(1, 4):
            self.text.emit(f'{i}')
            time.sleep(1)
        self.text.emit('网络已经成功还原！')

    def run(self):
        self.restore_network()


if __name__ == '__main__':
    rn = RestoreNetwork()
    rn.restore_network()
