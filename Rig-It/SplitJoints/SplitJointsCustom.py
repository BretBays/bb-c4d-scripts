"""
Split Joint Custom

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R12.021

Name-US: Split Joint Custom
Description-US: Evenly distributes a user defined number of joints to be placed in between 2 selected joints
"""


import c4d
from c4d import gui

def GetGlobalPosition(obj):
    return obj.GetMg().off
    

def SetGlobalPosition(obj, pos):
    m=obj.GetMg()
    m.off=pos
    return obj.SetMg(m)

def GetGlobalRotation(obj):
    return c4d.utils.MatrixToHPB(obj.GetMg())

def SetGlobalRotation(obj, rot):
    m=obj.GetMg()
    pos=m.off
    scale=c4d.Vector(m.v1.GetLength(), m.v2.GetLength(), m.v3.GetLength())

    m=c4d.utils.HPBToMatrix(rot)
    
    m.off=pos
    m.v1=c4d.Vector.GetNormalized(m.v1)*scale.x
    m.v2=c4d.Vector.GetNormalized(m.v2)*scale.y
    m.v3=c4d.Vector.GetNormalized(m.v3)*scale.z
    return obj.SetMg(m)


def lerp(a, b, t):
    val=a+(b-a)*t
    return val
    
class MyDialog(c4d.gui.GeDialog):
	value = 2 # Change this from 0 to 2 to avoid division by Zero Errors
	def CreateLayout(self):
		self.SetTitle("Split into How many Joints?")
		self.GroupBegin(999, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT)
		self.AddEditSlider(1000, c4d.BFH_LEFT)
		self.AddButton(1002, c4d.BFH_RIGHT, name="Close")
		self.GroupEnd()
		return True

	def Command(self, id, msg=None):
		if id==1002:
			self.Close()
		elif id==1000: #the slider ID!!
			#command is called on a user event, so when the slider was changed
			#we have to save the current value
			self.value = self.GetLong(1000)
	
		return True
	
	def InitValues(self):
	#1000 is the ID of the slider
	#2 is the default starting value of the slider
	#min=2 is the lowest value the slider can go to
	#max=30 is the highest value the slider can go to
		self.SetReal(1000, 2, min=2, max=30)

		return True

	def GetValue(self):
		return self.value

	def AskClose(self):
		return False


def main():
    doc.StartUndo()
    factor=0.0
    numJoints=[0]
    ObjList=doc.GetSelection()
    if len(ObjList)!=2:
        gui.MessageDialog("Please Select the 2 Objects you'd like to split between")

    else:
        ObjList=doc.GetSelection()
        StartJnt=ObjList[0]
        EndJnt=ObjList[1]
        window=MyDialog()
        window.Open(dlgtype=c4d.DLG_TYPE_MODAL_RESIZEABLE)
        value=window.GetValue()
        Startcolor=ObjList[0][c4d.ID_BASEOBJECT_COLOR]
        Endcolor=ObjList[1][c4d.ID_BASEOBJECT_COLOR]
                
        factor=100.0/value/100
            
        StartVec=StartJnt.GetAbsPos()
        EndVec=EndJnt.GetAbsPos()

        s=1
        while (s<=value):
            
            p=s-1

            pos=lerp(StartJnt.GetMg().off, EndJnt.GetMg().off, factor*s)
            numJoints.append(c4d.BaseObject(1019362))

#            numJoints[s].SetAbsPos(lerp(StartVec, EndVec, factor))
            numJoints[s][c4d.ID_BASEOBJECT_COLOR]=lerp(Startcolor, Endcolor, (factor*s))
            numJoints[s].SetName(StartJnt.GetName()+ "_" +str(0)+str(s))

            if s == 1:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, numJoints[s])
                doc.InsertObject(numJoints[s],StartJnt)
                SetGlobalPosition(numJoints[s], pos)
                SetGlobalRotation(numJoints[s], GetGlobalRotation(StartJnt))
            else:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, numJoints[s])
                doc.InsertObject(numJoints[s], numJoints[p]) 
                SetGlobalPosition(numJoints[s], pos)
                SetGlobalRotation(numJoints[s], GetGlobalRotation(StartJnt))

                            
            doc.AddUndo(c4d.UNDOTYPE_NEW, numJoints[s])
            s=s+1

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, EndJnt)
               
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, EndJnt)
        EndJnt.InsertUnder(numJoints[value-1])

        SetGlobalPosition(EndJnt, numJoints[value].GetMg().off)

        doc.AddUndo(c4d.UNDOTYPE_DELETE, numJoints[value])
        numJoints[value].Remove()   
     
    doc.EndUndo()
    c4d.EventAdd()

    
    

if __name__=='__main__':
    main()