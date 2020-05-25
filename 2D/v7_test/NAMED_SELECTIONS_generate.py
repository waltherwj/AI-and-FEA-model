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


##Creates named selections
Model.AddNamedSelection()  #Adds a named selection
number_of_ns = len( Model.NamedSelections.Children)
ns = Model.NamedSelections.Children[number_of_ns-1] #creates a temporary variable to store it
ns.ScopingMethod = GeometryDefineByType.Worksheet #changes the scoping method to be worksheet
## creates a criterion object and stores it
criterion = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion
#Criterion Options: active: bool, actionType: SelectionActionType, 
#entityType: SelectionType, criterionType: SelectionCriterionType, 
#operatorType: SelectionOperatorType, value: object, 
#lowerBound: Quantity, upperBound: Quantity, 
#coordinateSystem: CoordinateSystem

ns.GenerationCriteria.Add(criterion()) ##creates new empty selection criterion
#criterion(actionType = SelectionActionType.Add)
ns.GenerationCriteria[0].EntityType = SelectionType.MeshNode 


