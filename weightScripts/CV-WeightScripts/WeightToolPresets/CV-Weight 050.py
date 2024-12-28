"""
Name-US: CV-Weight 50%
Description-US: Set the Weight Strength Slider to 50%
"""
import c4d
from c4d import gui


def main():
    curTool_ID=doc.GetAction()
    c4d.CallCommand(1019499)
    WeightTool_ID=doc.GetAction()
    WeightTool=c4d.plugins.FindPlugin(WeightTool_ID, c4d.PLUGINTYPE_TOOL)
    WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=.5
    wmgr=c4d.modules.character.CAWeightMgr
    strength=wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, .5)
    c4d.CallCommand(curTool_ID)


if __name__=='__main__':
    main()