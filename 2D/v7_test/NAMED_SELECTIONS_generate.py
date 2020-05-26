import math
## Script to generate named selections for forces and displacements

##Delete Previous NS
for named_selection in Model.NamedSelections.Children:
    named_selection.Delete()

## Gets bounding box
part = Model.Geometry.Children[0]
body = part.Children[0]
geobody = body.GetGeoBody()
x1,y1,z1,x2,y2,z2 = geobody.GetBoundingBox() # [x1 y1 z1 x2 y2 z2] coordinates of the bounding box, lower to higher

## creates a criterion object and stores it
criterion = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion
#Criterion Options: active: bool, actionType: SelectionActionType, 
#entityType: SelectionType, criterionType: SelectionCriterionType, 
#operatorType: SelectionOperatorType, value: object, 
#lowerBound: Quantity, upperBound: Quantity, 
#coordinateSystem: CoordinateSystem

##Choose Number of forces
##Choose number of displacements

##Creates named selections
number_of_selections = 3
for i in range(number_of_selections):
    Model.AddNamedSelection()  #Adds a named selection
    number_of_ns = len( Model.NamedSelections.Children)
    ns = Model.NamedSelections.Children[number_of_ns-1] #creates a temporary variable to store it
    ns.ScopingMethod = GeometryDefineByType.Worksheet #changes the scoping method to be worksheet
    number_of_criteria = 3
   
    for i in range(number_of_criteria):
        ns.GenerationCriteria.Add(criterion()) ##creates new empty selection criterion
        ns.GenerationCriteria[i].EntityType = SelectionType.MeshNode
        ns.GenerationCriteria[i].CoordinateSystem = Model.CoordinateSystems.Children[0]
        if i == 0:
            ns.GenerationCriteria[i].Action =  SelectionActionType.Add
            ns.GenerationCriteria[i].Criterion =  SelectionCriterionType.LocationX
            ns.GenerationCriteria[i].Operator =  SelectionOperatorType.RangeInclude
        else:
            ns.GenerationCriteria[i].Action =  SelectionActionType.Filter
    


    ns.Generate()

