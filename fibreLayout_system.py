#-------------------------------------------------------------------------------
# Name:    fiber_layout_0502(system)
# Purpose: define fiber layout in ITECH pavilion
#
# Author:  Kantaro MAKANAE(referenced from Kenryo TAKAHASHI & Vangel KUKOV)
#
# Created: 02/05/2014
#-------------------------------------------------------------------------------

import rhinoscriptsyntax as rs
import math
import random



#set an agent
class Worm:
    def __init__(self, idStartPt, idNextPt, crvdeg, angle):
        self.step = 0
        self.idPrePt = idStartPt
        self.idCurrentPt = idNextPt
        self.listIdTrailPt = []
        self.listTrailPt3d = []
        self.listPtCrv = []
        self.crvdeg = crvdeg
        self.angledeg = angle
        self.listNextPt = []
        #add prepoint to the list
        self.listIdTrailPt.append(self.idPrePt)
        self.listTrailPt3d.append(dictSelVertices3d[self.idPrePt])


    def Move(self):
        
        listIdCanNextPt = dictNeighbors[self.idCurrentPt]
        
        setIdCanNextPt = set(listIdCanNextPt)
        setIdTrailPt = set(self.listIdTrailPt)
        
        setIdCanNextPt_2 = setIdCanNextPt - setIdTrailPt
        
        if not setIdCanNextPt_2:
            setIdCanNextPt_2 = setIdCanNextPt
        else:
            setIdCanNextPt_2 = setIdCanNextPt - setIdTrailPt
        
        listIdCanNextPt_2 = list(setIdCanNextPt_2)
        
        if not listIdCanNextPt_2:
            print "fuck off empty list"
        else:
            print "All's right with the world"
        
        listAngle = []
        #print len(listIdCanNextPt_2)
        #print dictSelVertices3d[listIdCanNextPt_2[0]]
        #print listIdCanNextPt_2[0]
        for i in range(len(listIdCanNextPt_2)):
            print listIdCanNextPt_2[i], "test"
            PtA = dictSelVertices3d[self.idCurrentPt]
            PtB = dictSelVertices3d[self.idPrePt]
            PtC = dictSelVertices3d[listIdCanNextPt_2[i]]
            vec1 = rs.VectorCreate(PtA, PtB)
            vec2 = rs.VectorCreate(PtA, PtC)
            angle = rs.VectorAngle(vec1, vec2)
            listAngle.append(angle)
        
        if not listAngle:
            print "listAngle : fuck off empty list"
        else:
            print "listAngle : All's right with the world"
        
        if len(listAngle) >= 2:
            del listIdCanNextPt_2[listAngle.index(max(listAngle))]
            del listAngle[listAngle.index(max(listAngle))]
        
        idNextPt = listIdCanNextPt_2[listAngle.index(max(listAngle))]
        
        #update PrePt & CurrentPt and add them to the lists
        self.idPrePt = self.idCurrentPt
        self.idCurrentPt = idNextPt
        self.listIdTrailPt.append(self.idCurrentPt)
        self.listTrailPt3d.append(dictSelVertices3d[self.idCurrentPt])
        
        #add step
        self.step += 1
        
        #draw CurrentPt
        point = rs.AddPoint(dictSelVertices3d[self.idCurrentPt])
        return point


    def Draw(self):
        
        #pick points for line drawing
        if self.step % self.crvdeg == 0:
                self.listPtCrv.append(dictSelVertices3d[self.idCurrentPt])
        
        #draw curve
        if self.step >= 2 * self.crvdeg:
            crvTrail = rs.AddCurve(self.listPtCrv)
        else:
            crvTrail = rs.AddCurve(self.listTrailPt3d)

        return crvTrail


#return selected/non-selected points id and point3d
def makeSelVertices_2(mesh,Pts,SelNum): 
    
    listVertices3d = rs.MeshVertices(mesh)
    
    idListVertices = []
    idListNotVertices = []
    for i in range(len(listVertices3d)):
        DisPts = rs.Distance(Pts, listVertices3d[i])
        if DisPts <= dist:
            idListVertices.append(i)
        else:
            idListNotVertices.append(i)
    
    
    selListVertices3d = []
    for k in idListVertices:
        selListVertices3d.append(listVertices3d[k])
    selDictVertices3d =  dict(zip(idListVertices, selListVertices3d))
    
    
    NOTselListVertices3d = []
    for j in idListNotVertices:
        NOTselListVertices3d.append(listVertices3d[j])
    NOTselDictVertices3d = dict(zip(idListNotVertices, NOTselListVertices3d))
    
    
    if SelNum == 0:
        return idListVertices
    elif SelNum == 1:
        return idListNotVertices
    elif SelNum == 2:
        return selListVertices3d
    elif SelNum == 3:
        return NOTselListVertices3d
    elif SelNum == 4:
        return selDictVertics3d
    elif SelNum == 5:
        return NOTselDictVertices3d


#get list of neighbors
def importPtListNeighbors(Mesh, Pts):
    
    dictNeighbors = {}
    
    listFaceVertices = rs.MeshFaceVertices(Mesh)
    
    idListNotVertices = makeSelVertices_2(Mesh,Pts,1)
    print "len-idListNotVertices", len(idListNotVertices)
    idListVertices = makeSelVertices_2(Mesh,Pts,0)
    #print "type of selListVertices3d", type(selListVertices3d)
    setidListVertices = set(idListVertices)
    
    #check neighbour for each vertex
    for idVer in idListNotVertices:
        listVerNeigh = [] 
        verNeighFaces = rs.MeshVertexFaces(Mesh, idVer) #make list of faces with eace vertices
        setVerNeigh = set([])
        for idFaces in verNeighFaces: #check by each face
            idVerPts = listFaceVertices[idFaces] #vertices list for each face
            for idPt in idVerPts:
                if idVer != idPt: #if it is not the vertex...
                    setVerNeigh.add(idPt) #add to set
            
        listVerNeigh = list(setVerNeigh - setidListVertices) #remove points which NOT included
        dictNeighbors[idVer] = listVerNeigh
        
    return dictNeighbors

#set initial position of the agent
def setInitial(aN,M,crvdeg, angle):
    
    worms = []
    
    #pick a naked edge points
    judgeIdEdgePt = rs.MeshNakedEdgePoints(M)
    IdEdgePts = []
    for j in range(len(judgeIdEdgePt)):
        if judgeIdEdgePt[j] == True:
            IdEdgePts.append(j)
    
    listSelIdEdgePts = []
    for k in range(len(IdEdgePts)):
        #if 0 <= IdEdgePts[k] <= 918:
        listSelIdEdgePts.append(IdEdgePts[k])
    
    #select startPt and nextPt from the list of naked edge points
    for i in range(aN):
        idStartPt = listSelIdEdgePts[random.randint(0, len(listSelIdEdgePts))]
        random.seed()
        idNextPt = dictNeighbors[idStartPt][random.randint(0, len(dictNeighbors[idStartPt])-1)]
        
        #make worm and add in list of worms
        worms.append( Worm(idStartPt, idNextPt, crvdeg, angle))
        
    return worms


#process
if reset == False:
    dictSelVertices3d = makeSelVertices_2(mesh,pts,5)
    print "len-dictSelVertices3d", len(dictSelVertices3d)
    dictNeighbors = importPtListNeighbors(mesh, pts)
    print "len-dictNeighbors", len(dictNeighbors)
    wormsInitial = setInitial(agentNum, mesh, crvdeg, angle)
    
    a = makeSelVertices_2(mesh,pts,2)
