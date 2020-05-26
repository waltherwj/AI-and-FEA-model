import math
import random
## Script to generate named selections for forces and displacements

##Delete Previous NS
for named_selection in Model.NamedSelections.Children:
    named_selection.Delete()
for i, coord_system in enumerate(Model.CoordinateSystems.Children):
    if i > 0: #to avoid global coord system
        coord_system.Delete()
        
## Gets bounding box
part = Model.Geometry.Children[0]
body = part.Children[0]
geobody = body.GetGeoBody()
x1,y1,z1,x2,y2,z2 = geobody.GetBoundingBox() # [x1 y1 z1 x2 y2 z2] coordinates of the bounding box, lower to higher
x1,y1,z1,x2,y2,z2 = x1*39.3701,y1*39.3701,z1*39.3701,x2*39.3701,y2*39.3701,z2 *39.3701
##Create coordinate systems with brownian motion
## Create direction of "guided" brownian motion

p_direction = [Quantity(random.uniform(x1,x2).ToString() + '[in]') - Quantity(random.uniform(x1,x2).ToString() + '[in]'),
               Quantity(random.uniform(y1,y2).ToString() + '[in]') - Quantity(random.uniform(y1,y2).ToString() + '[in]'),
               Quantity(random.uniform(z1,z2).ToString() + '[in]') - Quantity(random.uniform(z1,z2).ToString() + '[in]')]

number_created = 10
for i in range(number_created):
    number_coord = len(Model.CoordinateSystems.Children)
    Model.CoordinateSystems.AddCoordinateSystem()
    cs = Model.CoordinateSystems.Children[number_coord] #last coordinate system
    if i==0:
        cs.OriginX = Quantity(random.uniform(x1,x2).ToString() + '[in]')
        cs.OriginY = Quantity(random.uniform(y1,y2).ToString() + '[in]')
        cs.OriginZ = Quantity(random.uniform(z1,z2).ToString() + '[in]')
        X = cs.OriginX
        Y = cs.OriginY
        Z = cs.OriginZ
    else:
        X += (Quantity(random.uniform(x1,x2).ToString() + '[in]') + p_direction[0])/number_created
        Y += (Quantity(random.uniform(y1,y2).ToString() + '[in]') + p_direction[1])/number_created
        Z += (Quantity(random.uniform(z1,z2).ToString() + '[in]') + p_direction[2])/number_created
        cs.OriginX = X
        cs.OriginY = Y
        cs.OriginZ = Z


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

