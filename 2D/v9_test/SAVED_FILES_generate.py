## Creates solutions and exports them

## Load-in the body
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0] #Get  first body
geobody = body.GetGeoBody()
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.


## Delete previously assigned forces
analysis = Model.Analyses[0]
solution = analysis.Solution
deformation = []
number_directional_deformations = len(solution.GetChildren(DataModelObjectCategory.DirectionalDeformation, False))
while number_directional_deformations != 3:
    if number_directional_deformations < 3:
        number_directional_deformations =len(solution.GetChildren(DataModelObjectCategory.DirectionalDeformation, False))
        deformation.append(solution.AddDirectionalDeformation())
    if number_directional_deformations > 3:
        number_directional_deformations =len(solution.GetChildren(DataModelObjectCategory.DirectionalDeformation, False))
        solution.Children[1].Delete()
