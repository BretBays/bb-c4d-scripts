import c4d
from c4d import gui
#Welcome to the world of Python


def deleteAllAnimation(obj):
    if obj is None: return

    tracks=obj.GetCTracks()
    if len(tracks)>0:
        for track in tracks:
            doc.AddUndo(c4d.UNDOTYPE_DELETE, track)
            track.Remove()

    if obj.GetDown():
        deleteAllAnimation(obj.GetDown())
    if obj.GetNext():
        deleteAllAnimation(obj.GetNext())



def main():
    doc.StartUndo()
    c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD | c4d.DRAWFLAGS_STATICBREAK)
    obj=doc.GetFirstObject()
    deleteAllAnimation(obj)

    doc.EndUndo()
    c4d.EventAdd()



if __name__=='__main__':
    main()