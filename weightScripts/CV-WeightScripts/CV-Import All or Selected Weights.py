"""
Name-US: CV-Import All or Selected Weights...
Description-US: Import and apply all the weights from a directory or only apply to the selected objects
"""

import c4d
import os

joints = []
jointErr = []
vErr = []



def main():


    #Get Our directory
    fn=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select the Weights Folder", c4d.FILESELECT_DIRECTORY)

    #Get all the files in our directory
    files=os.listdir(fn)
    objs=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

    if len(objs)>0:
        tempList=[]
        for obj in objs:
            if obj.GetName() in files:
                tempList.append(obj.GetName())

        files=tempList

    for wFile in files:
        obj=doc.SearchObject(wFile)
        if obj and obj.GetType()==5100:
            weightlist = open(fn+str("/")+str(wFile), "r")
            weightTag = c4d.modules.character.CAWeightTag()
            obj.InsertTag(weightTag)

            for line in weightlist:
                thisLine = line.split()
                if len(thisLine) == 0 or line[0] == "#":
                  continue
                if thisLine[0] and thisLine[0] == "deformer":
                  thisJoint = doc.SearchObjectInc(thisLine[2])
                  if thisJoint == None:
                    jointErr.append(thisLine[2])
                  else:
                    joints.insert(int(thisLine[1]),thisLine[2])
                    jointIdx = weightTag.AddJoint(thisJoint)
                    if jointIdx != int(thisLine[1]):
                      print("Joint Index mismatch - " + thisLine[2] + "[" + thisLine[1] + "," + str(jointIdx) + "]")

                elif thisLine[0][-1] == ":":
                  v = int(thisLine[0][:-1])
                  if v > obj.GetPointCount():
                    vErr.append(v)
                  weightList = thisLine[1:]
                  i = 0
                  while i < len(weightList):
                      weightTag.SetWeight(int(weightList[i]), v, float(weightList[i+1]))
                      i = i + 2

            if len(jointErr) > 0 or len(vErr) > 0:
                print(jointErr)
                print(vErr)



        else:
            print("Sorry No Match")

        c4d.EventAdd()

if __name__=='__main__':
    main()