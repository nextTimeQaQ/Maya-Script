def select_attr_channels_in_graph_editor(attrs):
    graph_ed_outliner = cmds.editor("graphEditor1GraphEd",q=1,mainListConnection=1)
    cmds.selectionConnection(graph_ed_outliner,e=1,clear=1)
    sel = cmds.ls(sl=1)
    for i in sel:
        for attr in attrs:
            name_attr = "%s.%s"%(i,attr)
            if cmds.objExists(name_attr):
                cmds.selectionConnection(graph_ed_outliner,e=1,select=name_attr)
## select_attr_channels_in_graph_editor(["tx","tz","xxxx"])
