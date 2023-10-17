"""
Name-US:IncreaseWeightStrength
Description-US: Increase the strength of the Weights Manager, Paint Tool, and Weight tool. Without any modifiers
(ie CTRL and CTRL+SHIFT) will increase strength by 10%. With CTRL-5%, with CTRL+SHIFT-1%. 
When binding to a hotkey, use the same hot key with modifiers in the command manager
"""
import c4d
from c4d import gui

#TOOL IDS FOR LATER
PAINTTOOL=1021286
WEIGHTTOOL=1019499

def main():
    increment=.01

    #Get the modifier to know what % change we need to do.
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):

        #If CTRL is pressed, increment to 5%
        if bc[c4d.BFM_INPUT_QUALIFIER]== 2:
            increment=increment*5

        #if CTRL+SHIFT is pressed, we want precision, so leave it at 1
        elif bc[c4d.BFM_INPUT_QUALIFIER] == 3:
            increment=increment
        else:
            #Otherwise, let's go by 10%'
            increment = increment* 10

    #Store the current tool we have selected
    curTool_ID=doc.GetAction()

    #Get all of the necessary managers and tool instances
    wmgr=c4d.modules.character.CAWeightMgr
    WeightTool=c4d.plugins.FindPlugin(WEIGHTTOOL, c4d.PLUGINTYPE_TOOL)
    PaintTool=c4d.plugins.FindPlugin(PAINTTOOL, c4d.PLUGINTYPE_TOOL)

    #By default it will sync all of them to the Weight Managers strength
    strength=wmgr.GetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH)
    result=strength+increment

    #Conditional statements for clamping the strength values between 0.0-1.0(0% or 100%)
    if result>1.0:
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 1.0)
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=1.0
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=1.0
    elif result<0.0:
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, 0.0)
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=0.0
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=0.0
    else:
        wmgr.SetParameter(doc, c4d.ID_CA_WEIGHT_MGR_WEIGHT_STRENGTH, result)
        WeightTool[c4d.ID_CA_WEIGHT_TOOL_STRENGTH]=result
        PaintTool[c4d.ID_CA_PAINT_TOOL_OPACITY]=result

    #If theres a current tool ID stored, let's return to it.'
    if curTool_ID is None:
        return
    else:
        c4d.CallCommand(curTool_ID)


if __name__=='__main__':
    main()