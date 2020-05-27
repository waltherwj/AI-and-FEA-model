import math
import random
## Script to generate named selections for forces and displacements

##Delete Previous named selection and coordinate systems
try:
    for named_selection in Model.NamedSelections.Children:
        named_selection.Delete()
    for i, coord_system in enumerate(Model.CoordinateSystems.Children):
        if i > 0: #to avoid global coord system
            coord_system.Delete()
except:
    pass
## Gets bounding box
part = Model.Geometry.Children[0]
body = part.Children[0]
geobody = body.GetGeoBody()
x1,y1,z1,x2,y2,z2 = geobody.GetBoundingBox() # [x1 y1 z1 x2 y2 z2] coordinates of the bounding box, lower to higher
#x1,y1,z1,x2,y2,z2 = x1*39.3701,y1*39.3701,z1*39.3701,x2*39.3701,y2*39.3701,z2 *39.3701

##Create coord system at centroid for testing
"""
Model.CoordinateSystems.AddCoordinateSystem()
centroid = Model.CoordinateSystems.Children[1]
centroid.OriginX = Quantity(geobody.Centroid[0].ToString() + '[m]')
centroid.OriginY = Quantity(geobody.Centroid[1].ToString() + '[m]')
centroid.OriginZ = Quantity(geobody.Centroid[2].ToString() + '[m]')
"""

number_forces = random.choice(range(3))
number_displacements = random.choice(range(1,3))
number_of_curves = number_forces + number_displacements
for curve in range(number_of_curves):
    ## Choose one of the vertices as a starting point
    vertex_choice = random.choice(range(len(geobody.Vertices)))
    vertex = geobody.Vertices[vertex_choice]
    vertX = vertex.X
    vertY = vertex.Y
    vertZ = vertex.Z

##Create coordinate systems with biased brownian motion

    number_created = 5
    bias_control = 2
    
    for i in range(number_created):
        number_coord = len(Model.CoordinateSystems.Children)
        Model.CoordinateSystems.AddCoordinateSystem()
        cs = Model.CoordinateSystems.Children[number_coord] #last coordinate system
        if i==0:
            
            ## creates initial point close to a vertex but dislocated randomly within an elliptical radius based on the bounding box
            cs.OriginX = Quantity(random.uniform(x1,x2).ToString() + '[m]')/bias_control + Quantity(vertX.ToString() + '[m]')
            cs.OriginY = Quantity(random.uniform(y1,y2).ToString() + '[m]')/bias_control + Quantity(vertY.ToString() + '[m]')
            cs.OriginZ = Quantity(random.uniform(z1,z2).ToString() + '[m]')/bias_control + Quantity(vertZ.ToString() + '[m]')
            X = cs.OriginX
            Y = cs.OriginY
            Z = cs.OriginZ
           # print(X, Y, Z)
            ## create a random bias toward the centroid for the random movement 
            p_x = -(X - Quantity(geobody.Centroid[0].ToString() + '[m]'))
            p_y = -(Y - Quantity(geobody.Centroid[1].ToString() + '[m]'))
            p_z = -(Z - Quantity(geobody.Centroid[2].ToString() + '[m]'))
            dir_rand = 1.7
            p_direction = [p_x + dir_rand*Quantity(random.uniform(0,p_x.Value).ToString() + '[m]'),
                           p_y + dir_rand*Quantity(random.uniform(0,p_y.Value).ToString() + '[m]'),
                           p_z]
            ##scale it to be a unit vector
            p_abs = math.sqrt(p_direction[0].Value**2 + p_direction[1].Value**2 + p_direction[2].Value**2)
            p_direction = [p_direction[0]/p_abs, p_direction[1]/p_abs,p_direction[2]/p_abs,]
            
            #make sure the bias approaches the element initially
            dist_centr_initial = math.sqrt((X.Value-geobody.Centroid[0])**2 + 
                                           (Y.Value-geobody.Centroid[1])**2 + 
                                           (Z.Value-geobody.Centroid[2])**2)
            dist_centr_final = math.sqrt((X.Value+p_direction[0].Value/number_created-geobody.Centroid[0])**2 + 
                                         (Y.Value+p_direction[1].Value/number_created-geobody.Centroid[1])**2 + 
                                         (Z.Value+p_direction[2].Value/number_created-geobody.Centroid[2])**2)
            if dist_centr_initial < dist_centr_final:
                for i, direction in enumerate(p_direction):
                    p_direction[i] = p_direction[i]*(-1)
                    #print('entered')
    
        else:
            rand_control = 14
            distance_control = 40
            X += (Quantity(random.uniform(0,p_direction[0].Value).ToString() + '[m]')*rand_control + p_direction[0])/distance_control
            Y += (Quantity(random.uniform(0,p_direction[1].Value).ToString() + '[m]')*rand_control + p_direction[1])/distance_control
            Z += (Quantity(random.uniform(0,p_direction[2].Value).ToString() + '[m]')*rand_control + p_direction[2])/distance_control
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
    number_of_selections = number_created #makes the number of selections for this step the same as the number of coordinate systems created
    
    for i in range(number_of_selections):
        try:
            num_previous_selections = len(Model.NamedSelections.Children)
        except:
            num_previous_selections = 0
        Model.AddNamedSelection()  #Adds a named selection
        number_of_ns = len( Model.NamedSelections.Children)
        ns = Model.NamedSelections.Children[number_of_ns-1] #creates a temporary variable to store it
        ns.ScopingMethod = GeometryDefineByType.Worksheet #changes the scoping method to be worksheet
        number_of_criteria = num_previous_selections+1
        number_coordinates = len(Model.CoordinateSystems.Children)
        for ii in range(number_of_criteria):
            ns.GenerationCriteria.Add(criterion()) ##creates new empty selection criterion
            ns.GenerationCriteria[ii].EntityType = SelectionType.MeshNode
            
            ns.GenerationCriteria[ii].CoordinateSystem = Model.CoordinateSystems.Children[number_coordinates-number_created+i]
            if ii == 0:
                ns.GenerationCriteria[ii].Action =  SelectionActionType.Add
                ns.GenerationCriteria[ii].Criterion =  SelectionCriterionType.Distance
                ns.GenerationCriteria[ii].Operator =  SelectionOperatorType.LessThanOrEqual
                ns.GenerationCriteria[ii].Value = Quantity('0.12 [m]')
            else:
                ns.GenerationCriteria[ii].Action =  SelectionActionType.Filter
                ns.GenerationCriteria[ii].Criterion =  SelectionCriterionType.NamedSelection
                ns.GenerationCriteria[ii].Operator =  SelectionOperatorType.NotEqual
                ns.GenerationCriteria[ii].Value = Model.NamedSelections.Children[ii-1]
    
    
        ns.Generate()
    

size_increase = 1.3
for j, selection in enumerate(Model.NamedSelections.Children):
    selec = Model.NamedSelections.Children[j]
    while selec.TotalSelection == 0:
        selec.GenerationCriteria[0].Value = selec.GenerationCriteria[0].Value*size_increase
        selec.Generate()

