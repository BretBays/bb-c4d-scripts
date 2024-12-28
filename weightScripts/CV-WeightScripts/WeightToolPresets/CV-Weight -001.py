"""
Name-US: CV-Weight -1%
Description-US: Decrease the Weight Strength Slider by 1%
"""

import c4d
from c4d import gui


def main():
    curTool_ID=doc.GetAction()
    c4d.CallCommand(1019499)
    #We will get the weight manager and use it's strength as the basis for all 3 strengths
    wmgr=c4d.modules.character.CAWeightMgr
    strength=wmgr.GetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH)
    
    #Get the Weight Paint Tool and Paint Tool
    WeightTool_ID=doc.GetAction()
    WeightTool=c4d.plugins.FindPlugin(WeightTool_ID, c4d.PLUGINTYPE_TOOL)
    
    c4d.CallCommand(1021286)
    PaintTool_ID=doc.GetAction()
    PaintTool=c4d.plugins.FindPlugin(PaintTool_ID, c4d.PLUGINTYPE_TOOL)
    pStrength=PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]
    
    if strength==0:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=0
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 0)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=0
    elif strength-.01<0:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=0
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 0)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=0
    else:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=(strength-.01)
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, strength-.01)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=(strength-.01)

    if curTool_ID is None:
        return
    else:
        c4d.CallCommand(curTool_ID)


if __name__=='__main__':
    main()