import c4d

PAINTTOOL=1021286
WEIGHTTOOL=1019499

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
        #Store the current tool we have selected
    curTool_ID=doc.GetAction()

    #Get all of the necessary managers and tool instances
    wmgr=c4d.modules.character.CAWeightMgr
    WeightTool=c4d.plugins.FindPlugin(WEIGHTTOOL, c4d.PLUGINTYPE_TOOL)
    PaintTool=c4d.plugins.FindPlugin(PAINTTOOL, c4d.PLUGINTYPE_TOOL)

    wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_MODE, 5)
    WeightTool[c4d.ID_CA_WEIGHT_TOOL_MODE]= 5
    PaintTool[c4d.ID_CA_PAINT_TOOL_MODE]=5

    if curTool_ID is None:
        return
    else:
        c4d.CallCommand(curTool_ID)
        
    c4d.EventAdd()

if __name__ == '__main__':
    main()