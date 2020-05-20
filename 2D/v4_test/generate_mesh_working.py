part1 = Model.Geometry.Children[0] # Get the first part.
body1 = part1.Children[0] # Get the first body.
body = body1.GetGeoBody() # Cast to Geobody
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

selection.Entities = [body]  #  Add the body to the selection.

mesh_method = Model.Mesh.AddAutomaticMethod() # Adds the automatic method
mesh_method.Location = selection
mesh_method.ElementOrder = ElementOrder.Quadratic


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

