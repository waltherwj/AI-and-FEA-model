import random
import itertools

    ## Load-in the body
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0] #Get  first body
geobody = body.GetGeoBody()
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.


## Delete previously assigned forces
analysis = Model.Analyses[0]
for force in analysis.GetChildren(DataModelObjectCategory.NodalForce, False):
    force.Delete()
## Assign Material
part.Material = 'Structural Steel'

forces = []

##  set parameters
number_created = 5 ## can't find a way to trasmit this between scripts
number_selections = len(Model.NamedSelections.Children)//number_created
number_displacements = analysis.GetChildren(DataModelObjectCategory.NodalDisplacement, False)//number_created
number_forces = number_selections - number_displacements


for i in range(number_displacements, number_displacements + number_forces): #iterates displacement nodal selections
    for j in range(number_created):
        selection = named_selections[i][j]
        forces.append(analysis.AddNodalForce()) #creates displacement and store in list
        forces[-1].Location = selection #applies to named selection
    
        ## set values for displacements 
        components = []
        for ii in range(3): #create list of Quantities for displacements
            components.append(Quantity(random.gauss(0,100).ToString() + '[N]'))
        ## displacements for both 3d and 2d cases
        try:
            forces[-1].XComponent.Output.DiscreteValues = [components[0]]
            forces[-1].YComponent.Output.DiscreteValues = [components[1]]
            
            Is_3D = False
            for vertex in geobody.Vertices: #check if problem is 2d or 3d
                if vertex.Z != 0:
                    Is_3D = True
                    break
            if Is_3D: #displacement for 3d case
                forces[-1].ZComponent.Output.DiscreteValues = [components[2]]
            else:
                forces[-1].ZComponent.Output.DiscreteValues = [Quantity['0 [N]']]
        except IndexError:
            pass

