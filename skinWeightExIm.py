#!/usr/bin/python
# -*- coding: utf-8 -*-

## skin weight import and export
## 修改自 重庆_绑定_CRGlenn 2787723550
## 导出路径  self.path_text = cmds.textFieldGrp(l="Path:", tx=r"G:\file")
## 文件名称  self.file_name = cmds.textFieldGrp(l="File Name:", tx="testw")
## 导出选中模型的蒙皮权重


import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import json
from maya.api import OpenMaya, OpenMayaAnim
import pickle as pickle

class ExInSkin:
    def __init__(self):
        self.main_window = "ExInSkin"

        if cmds.window(self.main_window, ex=1):
            cmds.deleteUI(self.main_window, window=1)

        self.default = cmds.optionVar(q='saved_value')

        # crate new window
        self.crateNewWindow = cmds.window(self.main_window, t="ExInSkin V0.1",
                                          w=200, h=100)
        self.main_layout = cmds.formLayout(nd=100)

        self.path_text = cmds.textFieldGrp(l="Path:", tx=r"G:\file")
        self.file_name = cmds.textFieldGrp(l="File Name:", tx="testw")
        self.in_button = cmds.button(l="Import", c=self.ImportSkin)
        self.ex_button = cmds.button(l="Export", c=self.exportSkin)
        self.bar = cmds.progressBar(maxValue=100, width=200)
        self.result_tx = cmds.text(l="None")

        cmds.formLayout(self.main_layout, e=1,
                    af=([self.path_text, "right", 5],
                        [self.path_text, "left", 5]),
                    ac=([self.file_name, "top", 5, self.path_text],
                        [self.ex_button, "top", 5, self.file_name],
                        [self.in_button, "top", 5, self.ex_button],
                        [self.bar, "top", 5, self.in_button],
                        [self.result_tx, "top", 5, self.in_button],
                        [self.result_tx, "left", 5, self.bar]))

        cmds.showWindow(self.main_window)

        self.path = None



    def exportSkin(self, *args):
        geo = cmds.ls(sl=1, type="transform")[0]
        geo_cluster = mel.eval('findRelatedSkinCluster "{}"'.format(geo))
        num_vtxs = cmds.polyEvaluate(geo, v=True)
        vtx = cmds.ls("{}.vtx[*]".format(geo), fl=1)
        name = cmds.textFieldGrp(self.file_name, q=1, tx=1)

        sel_list = OpenMaya.MSelectionList()
        sel_list.add(geo)
        sel_list.add(geo_cluster)

        shape_dag = sel_list.getDagPath(0)
        skin_dep = sel_list.getDependNode(1)
        skin_fn = OpenMayaAnim.MFnSkinCluster(skin_dep)

        comp_ids = [c for c in range(num_vtxs)]
        single_fn = OpenMaya.MFnSingleIndexedComponent()
        shape_comp = single_fn.create(OpenMaya.MFn.kMeshVertComponent)
        single_fn.addElements(comp_ids)

        flat_weights, inf_count = skin_fn.getWeights(shape_dag, shape_comp)
        # print(flat_weights)
        # print(inf_count)
        weight_file = open("{}/{}.json".format(self.filePath(), name),"wb")
        pickle.dump(list(flat_weights),weight_file)
        weight_file.close()

        cmds.text(self.result_tx, e=1, l="Exported")

    def ImportSkin(self, *args):
        name = cmds.textFieldGrp(self.file_name, q=1, tx=1)

        with open("{}/{}.json".format(self.filePath(), name), "rb") as skin_file:
            flat_weights = pickle.load(skin_file)


        #comp_ids = sorted(load_skin)
        geo = cmds.ls(sl=1, type="transform")[0]
        geo_cluster = mel.eval('findRelatedSkinCluster "{}"'.format(geo))
        num_vtxs = cmds.polyEvaluate(geo, v=True)

        sel_list = OpenMaya.MSelectionList()
        sel_list.add(geo)
        sel_list.add(geo_cluster)

        shape_dag = sel_list.getDagPath(0)
        skin_dep = sel_list.getDependNode(1)
        skin_fn = OpenMayaAnim.MFnSkinCluster(skin_dep)

        comp_ids = [c for c in range(num_vtxs)]
        single_fn = OpenMaya.MFnSingleIndexedComponent()
        shape_comp = single_fn.create(OpenMaya.MFn.kMeshVertComponent)
        inf_dags = skin_fn.influenceObjects()
        inf_count = len(inf_dags)

        weights = OpenMaya.MDoubleArray(len(comp_ids) * inf_count, 0)
        inf_ids = OpenMaya.MIntArray()
        for i in range(inf_count):
            inf_ids.append(i)
        skin_fn.setWeights(shape_dag, shape_comp, inf_ids, OpenMaya.MDoubleArray(flat_weights), normalize=True)

        cmds.text(self.result_tx, e=1, l="Done!")

    def filePath(self, *args):
        self.path = cmds.textFieldGrp(self.path_text, q=1, tx=1)

        return self.path


ExInSkin()
