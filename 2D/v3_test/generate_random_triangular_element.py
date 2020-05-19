# Python Script, API Version = V18
import random
import math
from itertools import combinations
from System import Random

n_points = 4
n_dimensions = 3
points = []
curves = List[ITrimmedCurve]()
for i in range(n_points):   # creates all points
   points_temp = [0,0,0]
   for j in range(n_dimensions):
       if (j<=1 or i>2):
            points_temp[j] = (random.random() - 0.5)*2
            #random.jumpahead #scrambles the generated numbers to reduce correlation
           # print(random.getstate)
            
   points.append(points_temp)

# Delete Selection
try:
    selection = Selection.Create(GetRootPart().Bodies[:])
    result = Delete.Execute(selection)
except:
    pass
# EndBlock


for iter, x in enumerate(combinations(points, 3)): #iterates through all combinations of 3
    #print(iter)
    #curves = List[ITrimmedCurve]()
    for i in range(len(x)):  #iterates through points to create curves
            if i<2:
                #SketchPoint.Create(Point.Create(*x[i]))
                curveSegment = CurveSegment.Create(Point.Create(*x[i]), Point.Create(*x[i+1]))
                curves.Add(curveSegment)
            elif i==2:
                #SketchPoint.Create(Point.Create(*x[i]))
                curveSegment = CurveSegment.Create(Point.Create(*x[i]), Point.Create(*x[0]))   
                curves.Add(curveSegment)
            else:
                #print("else")
                SketchPoint.Create(Point.Create(MM(x[i][0]),MM(x[i][1]),MM(x[i][2])))    
    
    #Create Perpendicular Vector
    direc = []
    for ii in range(1,3):
       # print(x)
       # print(x[ii])
        direc_temp = [0,0,0]
        for jj, coord in enumerate(x[ii]):
            #print(ii)
            direc_temp[jj]= x[0][jj] - coord      
        direc.append(direc_temp)     
    a = Vector.Create(*direc[0])
    b = Vector.Create(*direc[1])
    perp_vec = Vector.Cross(a, b)
    #Create frame with perpendicular vector
    p = Point.Create(*x[0])
    frame = Frame.Create(p, perp_vec.Direction)    
    #print(perp_vec.Direction)
    #print(x)
    if iter==0:
        plane = Plane.PlaneXY
    else:
        plane = Plane.Create(frame)
        
    designResult = PlanarBody.Create(plane, curves) #creates the curve
    designBody = designResult.CreatedBody

if n_points >= 4:
    selec =[]
    for surf in GetRootPart().Bodies[:]: #transforms array of surfaces into list of surfaces
        selec.append(surf)
    targets = Selection.Create(*selec) #merges them
    result = Combine.Merge(targets)
    
# EndBlock

# Rename 'temp 1' to 'Body'
    selection = Selection.Create(GetRootPart().Bodies[0])
    result = RenameObject.Execute(selection,"Body")
# EndBlock

#ViewHelper.ZoomToEntity()

# Solidify Sketch
#mode = InteractionMode.Solid
#result = ViewHelper.SetViewMode(mode, None)
# EndBlock
