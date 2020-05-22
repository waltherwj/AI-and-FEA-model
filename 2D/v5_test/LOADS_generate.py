import random
import itertools
    ## Load in the body
    
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0].GetGeoBody() #Get geometrical entities of first body
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

    ## Create vector conditions
    
n_vertices = len(body.Vertices)
displaced_vertices = random.choice(range(0, n_vertices+1)) #number of vertices w/ a boundary displacement condition
choose_vertices = []
vert_chosen = [1] * displaced_vertices
vert_not_chosen = [0] * (n_vertices-displaced_vertices)
choose_vertices = vert_chosen + vert_not_chosen
random.shuffle(choose_vertices) #shuffles the list to not always choose the first vertices

for i, vertex in enumerate(body.Vertices):
    if choose_vertices[i] = 1:
        selection.Entities = [vertex]
        Model.Analyses[0].AddDs
    
## Create list of edges


