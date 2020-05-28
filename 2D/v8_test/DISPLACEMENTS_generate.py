import random
import itertools
import time

#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

    ## General Analysis Settings
settings = Model.Analyses[0].AnalysisSettings
settings.LargeDeflection = False
settings.WeakSprings = WeakSpringsType.ProgramControlled
settings.StoreResultsAt =  TimePointsOptions.LastTimePoints

## Create vector with all selections divided by curve
named_selections = []
number_rows = number_created
number_columns = number_forces + number_displacements
for i in range(number_columns):
    selec_temp = []
    for j in range(number_rows):
        selec_temp.append(Model.NamedSelections.Children[i*number_rows+j])
    named_selections.append(selec_temp)

    ## Delete conditions from previous analysis
analysis = Model.Analyses[0]
for disp in analysis.GetChildren(DataModelObjectCategory.Displacement, False):
    disp.Delete()
for fixed in analysis.GetChildren(DataModelObjectCategory.FixedSupport, False):
    fixed.Delete()

    ## Set displacement locations & values
displacements = []
for i in range(number_displacements): #iterates displacement nodal selections
    for  j in range(number_created):
        selection = named_selections[i][j]
        displacements.append(analysis.AddNodalDisplacement()) #creates displacement and store in list
        displacements[-1].Location = selection #applies to named selection
    
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



