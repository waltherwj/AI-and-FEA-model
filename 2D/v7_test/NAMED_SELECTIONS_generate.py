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
#x1,y1,z1,x2,y2,z2 = x1*39.3701,y1*39.3701,z1*39.3701,x2*39.3701,y2*39.3701,z2 *39.3701

## Choose one of the vertices as a starting point
vertex_choice = random.choice(range(len(geobody.Vertices)))
vertex = geobody.Vertices[vertex_choice]
vertX = vertex.X
vertY = vertex.Y
vertZ = vertex.Z

##Create coord system at centroid for testing
Model.CoordinateSystems.AddCoordinateSystem()
centroid = Model.CoordinateSystems.Children[1]
centroid.OriginX = Quantity(geobody.Centroid[0].ToString() + '[m]')
centroid.OriginY = Quantity(geobody.Centroid[1].ToString() + '[m]')
centroid.OriginZ = Quantity(geobody.Centroid[2].ToString() + '[m]')

##Create coordinate systems with biased brownian motion

number_created = 3
bias_control = 5
for i in range(number_created):
    number_coord = len(Model.CoordinateSystems.Children)
    Model.CoordinateSystems.AddCoordinateSystem()
    cs = Model.CoordinateSystems.Children[number_coord] #last coordinate system
    if i==0:
        
        cs.OriginX = Quantity(random.uniform(x1,x2).ToString() + '[m]')/bias_control + Quantity(vertX.ToString() + '[m]')
        cs.OriginY = Quantity(random.uniform(y1,y2).ToString() + '[m]')/bias_control + Quantity(vertY.ToString() + '[m]')
        cs.OriginZ = Quantity(random.uniform(z1,z2).ToString() + '[m]')/bias_control + Quantity(vertZ.ToString() + '[m]')
        X = cs.OriginX
        Y = cs.OriginY
        Z = cs.OriginZ
        p_direction = [-(X - Quantity(geobody.Centroid[0].ToString() + '[m]')),
                       -(Y - Quantity(geobody.Centroid[1].ToString() + '[m]')),
                       -(Z - Quantity(geobody.Centroid[2].ToString() + '[m]'))]

    else:
                #make sure the bias approaches the element initially
        dist_centr_initial = math.sqrt((X.Value-geobody.Centroid[0])**2 + 
                                       (Y.Value-geobody.Centroid[1])**2 + 
                                       (Z.Value-geobody.Centroid[2])**2)
        dist_centr_final = math.sqrt((X.Value+p_direction[0].Value-geobody.Centroid[0])**2 + 
                                     (Y.Value+p_direction[1].Value-geobody.Centroid[1])**2 + 
                                     (Z.Value+p_direction[2].Value-geobody.Centroid[2])**2)
        if dist_centr_initial < dist_centr_final:
            for i, direction in enumerate(p_direction):
                p_direction[i] = p_direction[i]*(-1)
                print('entered')

        X += (Quantity(random.uniform(0,p_direction[0].Value).ToString() + '[m]') + p_direction[0]/bias_control)/number_created
        Y += (Quantity(random.uniform(0,p_direction[1]).ToString() + '[m]') + p_direction[1]/bias_control)/number_created
        Z += (Quantity(random.uniform(0,p_direction[2]).ToString() + '[m]') + p_direction[2]/bias_control)/number_created
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

