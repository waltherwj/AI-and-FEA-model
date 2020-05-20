# Python Script, API Version = V18
import random
import math
from itertools import combinations, product, izip
from System import Random

n_points = 4
n_dimensions = 3
points = []
curves = List[ITrimmedCurve]()
for i in range(n_points):   # creates all points
    points_temp = [0,0,0]
    for j in range(n_dimensions):
        random.seed()
        if (j<=1) and i>0:
            points_temp[j] = random.random()
        elif (i>2):
            points_temp[j] = random.gauss(1,0.2)
            
    points.append(points_temp)
    


#choose quadrant
iter_quad = product([1, -1], repeat = 3)
quadrant  = []
for quad in iter_quad:
    quadrant.append(quad)
choice = random.choice(range(0,8))
choice=0
for i, point in enumerate(points):
    for j, coord in enumerate(point):
        points[i][j] = coord*quadrant[choice][j]



# Delete Selection
try:
    selection = Selection.Create(GetRootPart().Bodies[:])
    result = Delete.Execute(selection)
except:
    pass
try:
    selection = Selection.Create(GetRootPart().Curves[:])
    result = Delete.Execute(selection)
except:
    pass
# EndBlock

# create points for named selection
for point in points:
    print(point)
    SketchPoint.Create(Point.Create(*point))

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

ViewHelper.ZoomToEntity()

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

### NAMED SELECTIONS

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "element")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Curves[0])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "origin_node")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Curves[3])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "top_node")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Curves[1])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "plane_node_1")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Curves[2])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "plane_node_2")
# EndBlock


# NAME EDGES

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0].Edges[3])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "edge_closest")
# EndBlock


# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0].Edges[0])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "edge_plane_1")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0].Edges[2])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "edge_plane_2")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0].Edges[5])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "edge_far_1")
# EndBlock

# Create Named Selection Group
primarySelection = Selection.Create(GetRootPart().Bodies[0].Edges[1])
secondarySelection = Selection()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Group2", "edge_far_2")
# EndBlock