import random
import itertools

    ## Load-in the body
    
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0].GetGeoBody() #Get geometrical entities of first body
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.


## Delete previously assigned forces
analysis = Model.Analyses[0]
for force in analysis.GetChildren(DataModelObjectCategory.Force, False):
    force.Delete()

## Create edge forces

## Create vector to chose edges
n_edges = len(body.Edges)
n_loaded_edges = random.choice(range(0, n_edges+1)) #number of vertices w/ a boundary displacement condition
choose_edges = []
edge_chosen = [True] * n_loaded_edges
edge_not_chosen = [False] * (n_edges-n_loaded_edges)
choose_edges = edge_chosen + edge_not_chosen
random.shuffle(choose_edges) #shuffles the list to not always choose the first vertices

forces = []
for i, edge in enumerate(body.Edges):
    selection.Entities = [edge]
    if choose_edges[i]:
        forces.append(analysis.AddForce())
        forces[-1].Location = selection
    
    
    
    
