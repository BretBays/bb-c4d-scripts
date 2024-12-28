"""
Name-US: CV-Weight +5%
Description-US: Increase the Weight Strength Slider by 5%
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

    if strength==1.0:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=1
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 1)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=1
    elif strength+.05>1:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=1
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 1)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=1
    else:
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=(strength+.05)
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, strength+.05)
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=(strength+.05)

    if curTool_ID is None:
        return
    else:
        c4d.CallCommand(curTool_ID)



if __name__=='__main__':
    main()