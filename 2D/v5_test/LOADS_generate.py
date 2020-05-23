import random
import itertools
    ## Load-in the body
    
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0].GetGeoBody() #Get geometrical entities of first body
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

    ## General Analysis Settings
settings = Model.Analyses[0].AnalysisSettings
settings.LargeDeflection = True
settings.WeakSprings = WeakSpringsType.ProgramControlled
    ## Create vector conditions
    
n_vertices = len(body.Vertices)
displaced_vertices = random.choice(range(0, n_vertices+1)) #number of vertices w/ a boundary displacement condition
choose_vertices = []
vert_chosen = [True] * displaced_vertices
vert_not_chosen = [False] * (n_vertices-displaced_vertices)
choose_vertices = vert_chosen + vert_not_chosen
random.shuffle(choose_vertices) #shuffles the list to not always choose the first vertices

    ## Delete displacements from previous analysis
analysis = Model.Analyses[0]
for disp in analysis.GetChildren(DataModelObjectCategory.Displacement, False):
    disp.Delete()

displacements = []
ii=0

for i, vertex in enumerate(body.Vertices): #iterates vertices
    if choose_vertices[i]: #chooses correct vertices
        selection.Entities = [vertex]
        displacements.append(Model.Analyses[0].AddDisplacement()) #creates displacement and store in list
        displacements[-1].Location = selection #applies to vertex
    
    ## set values for displacements 
    components = []
    for j in range(3): #create list of strings for displacements
        components.append(Quantity(random.gauss(0,1).ToString() + '[in]'))
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
        
    
## Create list of edges


