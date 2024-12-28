"""
Name-US: CV-Import Weights Custom...
Description-US: Import the weights of an object with a custom file name
"""

import c4d

joints = []
jointErr = []
vErr = []

def main():
    if op==None or op.CheckType(c4d.Opolygon)==False:
       c4d.gui.MessageDialog("Error: Please select the polygonal object to weight")
       return

    fn = c4d.storage.LoadDialog(c4d.FSTYPE_ANYTHING, "Select Joint Weights File")
    if fn!=None:
      weightlist = open(fn, "r")

      weightTag = c4d.modules.character.CAWeightTag()
      op.InsertTag(weightTag)

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
          if v > op.GetPointCount():
            vErr.append(v)
          weightList = thisLine[1:]
          #print weightList
          i = 0
          while i < len(weightList):
              weightTag.SetWeight(int(weightList[i]), v, float(weightList[i+1]))
              i = i + 2

      if len(jointErr) > 0 or len(vErr) > 0:
        print(jointErr)
        print(vErr)

      c4d.EventAdd(0)

if __name__=='__main__':
    main()