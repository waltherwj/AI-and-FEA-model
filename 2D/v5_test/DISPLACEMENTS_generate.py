import random
import itertools
import time
    ## Load-in the body
    
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0].GetGeoBody() #Get geometrical entities of first body
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

    ## General Analysis Settings
    
settings = Model.Analyses[0].AnalysisSettings
settings.LargeDeflection = True
settings.WeakSprings = WeakSpringsType.ProgramControlled
settings.StoreResultsAt =  TimePointsOptions.LastTimePoints

    ## Create vector to choose vertices
n_vertices = len(body.Vertices)
displaced_vertices = random.choice(range(0, n_vertices+1)) #number of vertices w/ a boundary displacement condition
choose_vertices = []
vert_chosen = [True] * displaced_vertices
vert_not_chosen = [False] * (n_vertices-displaced_vertices)
choose_vertices = vert_chosen + vert_not_chosen
random.shuffle(choose_vertices) #shuffles the list to not always choose the first vertices

    ## Delete conditions from previous analysis
analysis = Model.Analyses[0]
for disp in analysis.GetChildren(DataModelObjectCategory.Displacement, False):
    disp.Delete()
for fixed in analysis.GetChildren(DataModelObjectCategory.FixedSupport, False):
    fixed.Delete()

    ## Set displacement locations & values
displacements = []
for i, vertex in enumerate(body.Vertices): #iterates vertices
    if choose_vertices[i]: #chooses correct vertices
        selection.Entities = [vertex]
        displacements.append(analysis.AddDisplacement()) #creates displacement and store in list
        displacements[-1].Location = selection #applies to vertex
    
    ## set values for displacements 
    components = []
    for j in range(3): #create list of strings for displacements
        components.append(Quantity(random.gauss(0,0.01).ToString() + '[in]'))
    ## displacements for both 3d and 2d cases
    try:
        displacements[-1].XComponent.Output.DiscreteValues = [components[0]]
        displacements[-1].YComponent.Output.DiscreteValues = [components[1]]
        
        Is_3D = False
        for vertex in body.Vertices: #check if problem is 2d or 3d
            if vertex.Z != 0:
                Is_3D = True
                break
        if Is_3D: #displacement for 3d case
            displacements[-1].ZComponent.Output.DiscreteValues = [components[2]]
        else:
            displacements[-1].ZComponent.Output.DiscreteValues = [Quantity['0 [in]']]
    except IndexError:
        pass
## Handling case of no vertex diplacements
if not any(choose_vertices):
    fixed = []
    while not any(choose_vertices): #while choose vertices has no True values
        for i, vertex in enumerate(choose_vertices):
            choose_vertices[i] = (random.random()<0.5)
    for i, vertex in enumerate(body.Vertices):
        if choose_vertices[i]:
            selection.Entities = [vertex]
            fixed.append(analysis.AddFixedSupport())
            fixed[-1].Location = selection


