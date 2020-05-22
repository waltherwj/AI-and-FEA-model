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
for i, vertex in enumerate(body.Vertices):
    if choose_vertices[i]:
        selection.Entities = [vertex]
        displacements.append(Model.Analyses[0].AddDisplacement())
        displacements[ii].Location = selection
        ii += 1
        
    
## Create list of edges


