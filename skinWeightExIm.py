#!/usr/bin/python
# -*- coding: utf-8 -*-

## skin weight import and export
## 修改自 重庆_绑定_CRGlenn 2787723550
## 导出路径  self.path_text = cmds.textFieldGrp(l="Path:", tx=r"G:\file")
## 文件名称  self.file_name = cmds.textFieldGrp(l="File Name:", tx="testw")
## 导出选中模型的蒙皮权重
## 导出当前选中模型的第一个模型的权重，权重写出只写出权重数据，不包含骨骼数量，顺序，名称，导入也是相同

import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import json
from maya.api import OpenMaya, OpenMayaAnim
import pickle as pickle

class ExInSkin:
    def __init__(self,file_path,e_i):
        self.file_path = file_path
        self.e_i = e_i

    def exportSkin(self, *args):
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
        single_fn.addElements(comp_ids)
        flat_weights, inf_count = skin_fn.getWeights(shape_dag, shape_comp)
        weight_file = open(self.file_path,"wb")
        pickle.dump(list(flat_weights),weight_file)
        weight_file.close()

    def ImportSkin(self, *args):
        
        with open(self.file_path, "rb") as skin_file:
            flat_weights = pickle.load(skin_file)

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
        inf_ids = OpenMaya.MIntArray()
        for i in range(inf_count):
            inf_ids.append(i)
        skin_fn.setWeights(shape_dag, shape_comp, inf_ids, OpenMaya.MDoubleArray(flat_weights), normalize=True)

    def main(self):
        if self.e_i is 0:
            self.exportSkin()
        else:
            self.ImportSkin()

# ex_w = ExInSkin(r"D:\file\test.weight",0)
# ex_w.main()
## 导出权重


# im_w = ExInSkin(r"D:\file\test.weight",1)
# im_w.main()
## 导入权重
