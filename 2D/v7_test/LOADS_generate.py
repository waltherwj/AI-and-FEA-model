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
for body_force in analysis.GetChildren(DataModelObjectCategory.Acceleration, False):
    body_force.Delete()
    
## Assign Material
part.Material = 'Structural Steel'

## Create vector to chose edges
n_edges = len(body.Edges)
n_loaded_edges = random.choice(range(0, n_edges+1)) #number of vertices w/ a boundary displacement condition
choose_edges = []
edge_chosen = [True] * n_loaded_edges
edge_not_chosen = [False] * (n_edges-n_loaded_edges)
choose_edges = edge_chosen + edge_not_chosen
random.shuffle(choose_edges) #shuffles the list to not always choose the first vertices

## Create vector to choose vertices
n_vertices = len(body.Vertices)
n_loaded_vertices = random.choice(range(0, n_vertices+1)) #number of vertices w/ a boundary displacement condition
choose_vertices = []
vertices_chosen = [True] * n_loaded_vertices
vertices_not_chosen = [False] * (n_vertices-n_loaded_vertices)
choose_vertices = vertices_chosen + vertices_not_chosen
random.shuffle(choose_vertices) #shuffles the list to not always choose the first vertices

forces = []
for i, edge in enumerate(body.Edges): # forces on edges
    selection.Entities = [edge]
    if choose_edges[i]:
        forces.append(analysis.AddForce())
        forces[-1].Location = selection
        # create forces
        force_magnitudes = [random.gauss(0,100), random.gauss(0,100), random.gauss(0,100000)]
        forces[-1].DefineBy = LoadDefineBy.Components
        forces[-1].XComponent.Output.DiscreteValues = [Quantity(force_magnitudes[0].ToString() + '[N]')]
        forces[-1].YComponent.Output.DiscreteValues = [Quantity(force_magnitudes[1].ToString() + '[N]')]
        
        Is_3D= False
        for vertex in body.Vertices: #check if problem is 2d or 3d
            if vertex.Z != 0:
                Is_3D = True
                break
        if Is_3D:
            forces[-1].ZComponent.Output.DiscreteValues = [Quantity(force_magnitudes[2].ToString() + '[N]')]
        else:
            forces[-1].ZComponent.Output.DiscreteValues = [Quantity('0 [N]')]
"""
for i, vertex in enumerate(body.Vertices):
    selection.Entities = [vertex]
    if choose_vertices[i]:
        forces.append(analysis.AddForce())
        forces[-1].Location = selection
        # create forces
        force_magnitudes = [random.gauss(0,100000), random.gauss(0,100000), random.gauss(0,100000)]
        forces[-1].DefineBy = LoadDefineBy.Components
        forces[-1].XComponent.Output.DiscreteValues = [Quantity(force_magnitudes[0].ToString() + '[N]')]
        forces[-1].YComponent.Output.DiscreteValues = [Quantity(force_magnitudes[1].ToString() + '[N]')]
        
        Is_3D= False
        for vertex in body.Vertices: #check if problem is 2d or 3d
            if vertex.Z != 0:
                Is_3D = True
                break
        if Is_3D:
            forces[-1].ZComponent.Output.DiscreteValues = [Quantity(force_magnitudes[2].ToString() + '[N]')]
        else:
            forces[-1].ZComponent.Output.DiscreteValues = [Quantity('0 [N]')]
            
""""
# apply body force 

selection.Entities = [body]
forces.append(analysis.AddAcceleration())
force_magnitudes = [random.gauss(0,300000), random.gauss(0,300000), random.gauss(0,300000)]
forces[-1].DefineBy = LoadDefineBy.Components
forces[-1].XComponent.Output.DiscreteValues = [Quantity(force_magnitudes[0].ToString() + '[in s^-2]')]
forces[-1].YComponent.Output.DiscreteValues = [Quantity(force_magnitudes[1].ToString() + '[in s^-2]')]
        
Is_3D= False
for vertex in body.Vertices: #check if problem is 2d or 3d
    if vertex.Z != 0:
        Is_3D = True
        break
if Is_3D:
    forces[-1].ZComponent.Output.DiscreteValues = [Quantity(force_magnitudes[2].ToString() + '[in s^-2]')]
else:
    forces[-1].ZComponent.Output.DiscreteValues = [Quantity('0 [in s^-2]')]
