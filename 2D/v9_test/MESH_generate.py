part1 = Model.Geometry.Children[0] # Get the first part.
body1 = part1.Children[0] # Get the first body.
body = body1.GetGeoBody() # Cast to Geobody
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

selection.Entities = [body]  #  Add the body to the selection.
body1.NonlinearEffects = True # Enable Non Linear  effects
##   deletes previous mesh
#    note: [0] because deleting moves the list up
try:
    for i in range(len(Model.Mesh.Children)):
        Model.Mesh.Children[0].Delete() 
except: 
    pass

mesh_method = Model.Mesh.AddAutomaticMethod() # Adds the automatic method
#Model.Mesh.Siz
mesh_method.Location = selection

#Properties
mesh_method.Method = MethodType.HexDominant
mesh_method.ElementOrder = ElementOrder.Quadratic

# General Mesh Settings
mesh = Model.Mesh
mesh.Resolution = 4

# Corner node refinement
vertex_size = []

for i, corner in enumerate(body.Vertices):
    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.
    selection.Entities= [corner]
    vertex_size.append(Model.Mesh.AddSizing())
    vertex_size[i].Location = selection
    vertex_size[i].SphereRadius = Quantity('300 [mm]')
    vertex_size[i].ElementSize = Quantity('1 [in]')

#Generate Mesh
Model.Mesh.GenerateMesh()



#gets body
#elementID = geometry.Children[0].ObjectId

#ElementSel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)

#ElementSel = elementID

#mesh_method = Model.AddMeshEdit.
#
#if len(Model.NamedSelections.Children)>4:
#    pass

#"""The following example creates a pressure on the first face of the first body for the first part."""
#pressure = Model.Analyses[0].AddPressure() # Add a pressure.
#part1 = Model.Geometry.Children[0]  # Get the first part.
#body1 = part1.Children[0]  # Get the first body.
#face1 = body1.GetGeoBody().Faces[0]  # Get the first face of the body.
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.
#selection.Entities = [face1]  #  Add the face to the selection.
#pressure.Location = selection  # Assign the selection to the pressure.
#pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]  # Set the time values.
#pressure.Magnitude.Output.DiscreteValues = [Quantity("10 [Pa]"), Quantity("20 [Pa]")]  # Set the magnitudes.

