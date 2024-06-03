#!/usr/bin/python
# -*- coding: utf-8 -*-

## skin weight import and export
## 修改自 重庆_绑定_CRGlenn 2787723550

## 导出模型权重：
## 参数1：权重文件路径
## 参数2：0为导出，1为导入
## 参数3：模型名称
## 权重写出只写出权重数据，不包含骨骼数量，顺序，名称，导入也是相同


import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import json
from maya.api import OpenMaya, OpenMayaAnim
import pickle as pickle

class ExInSkin:
    def __init__(self,file_path,e_i,geo):
        self.file_path = file_path
        self.e_i = e_i
        self.geo = geo

    def exportSkin(self, *args):
        # geo = cmds.ls(sl=1, type="transform")[0]
        geo = self.geo
        print(geo)
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
        with open(self.file_path,"wb") as f:
            pickle.dump(list(flat_weights),f)

    def ImportSkin(self, *args):
        
        with open(self.file_path, "rb") as skin_file:
            flat_weights = pickle.load(skin_file)

        # geo = cmds.ls(sl=1, type="transform")[0]
        geo = self.geo
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


# ex_w = ExInSkin(r"G:\file\test.weight",0,"model_name")
# ex_w.main()
## 导出权重


# im_w = ExInSkin(r"G:\file\test.weight",1,"model_name")
# im_w.main()
## 导入权重

