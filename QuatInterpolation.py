from maya import cmds, mel
import maya.api.OpenMaya as om

def get_MTransform(obj_name):
    sel = om.MSelectionList()
    sel.add(obj_name)
    mDagPath =sel.getDagPath(0)
    transformFunc = om.MFnTransform(mDagPath) 
    return transformFunc
    
def get_quat_from_mTrsM(transform_f,space):
    return transform_f.rotation(space,1)

def quat_interpolation(obj_name,space,start_time,end_time):
    cmds.currentTime(start_time)
    start_quat = get_quat_from_mTrsM(get_MTransform(obj_name),space)
    cmds.currentTime(end_time)
    end_quat = get_quat_from_mTrsM(get_MTransform(obj_name),space)
    all_frame = end_time-start_time
    if all_frame <= 1:
        return
    step_value = 1.0/all_frame
    
    for f in range(1,all_frame):
        curretn_frame = start_time+f
        cmds.currentTime(curretn_frame)
        t = f*step_value
        quat_f = om.MQuaternion.slerp(start_quat,end_quat,t)
        if space == 4:
            cmds.xform(obj_name,ws=1,m=quat_f.asMatrix())
        else:
            cmds.xform(obj_name,ws=0,m=quat_f.asMatrix())
        cmds.setKeyframe(obj_name,at="rotate",t=curretn_frame)

## quat_interpolation("locator1",om.MSpace.kObject,2,15)
四元数插值
第一个参数为对象
第二个为坐标空间，om.MSpace.kObject 局部坐标，om.MSpace.kWorld 世界坐标
第三个开始帧
第四个结束帧
