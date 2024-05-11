#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2024/4/11_16:47
# @File : vst_gui.py
# @Name : junyu
# @Software(IDE) : PyCharm
# 修改junyu，直接用maya cmds完成虚拟约束,不借助外部的库 先选父物体 再选子物体

from maya.OpenMayaUI import MQtUtil
from shiboken2 import wrapInstance
import maya.api.OpenMaya as om
import maya.cmds as cmds

from PySide2.QtWidgets import *
from PySide2.QtCore import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.select_obj = None
        self.offset_m = None
        self.resize(300, 100)
        self.setParent(wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u"虚拟约束插件")

        self.p1 = QPushButton(parent=self)
        self.p1.setText(u"记录位置")
        self.p1.clicked.connect(self.create_virtual_const)

        self.p2 = QPushButton(parent=self)
        self.p2.setText(u"应用")
        self.p2.clicked.connect(self.exec_virtual_const)

        # 垂直布局管理
        self.qv_main_layout_01 = QVBoxLayout()
        self.qv_main_layout_01.setSpacing(0)

        # 添加布局
        self.qv_main_layout_01.addWidget(self.p1)
        self.qv_main_layout_01.addWidget(self.p2)
        self.setLayout(self.qv_main_layout_01)

    def create_virtual_const(self):
        self.select_obj = cmds.ls(sl=True, type="transform")
        if len(self.select_obj) != 2:
            om.MGlobal.displayWarning(u"请选择两个物体, 然后重新运行")
            self.select_obj = None
            return None
        cild_ws_m = cmds.xform(self.select_obj[1],ws=1,m=1,q=1)
        parent_ws_m = cmds.xform(self.select_obj[0],ws=1,m=1,q=1)
        self.offset_m = om.MMatrix(cild_ws_m) * om.MMatrix(parent_ws_m).inverse()
        #print(self.offset_m)
        om.MGlobal.displayInfo(u"记录完成")

    def exec_virtual_const(self):
        parent_ws_m = cmds.xform(self.select_obj[0],ws=1,m=1,q=1)
        ret = self.offset_m * om.MMatrix(parent_ws_m)
        #print(ret)
        cmds.xform(self.select_obj[1],ws=1,m=ret)


def run():
    w = MainWindow()
    w.show()
run()
