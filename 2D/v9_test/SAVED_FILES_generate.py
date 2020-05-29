## Creates solutions and exports them

## Load-in the body
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0] #Get  first body
geobody = body.GetGeoBody()
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.


## Delete previously assigned forces
analysis = Model.Analyses[0]
solution = analysis.Solution
"""
number_directional_deformations = len(solution.GetChildren(DataModelObjectCategory.DirectionalDeformation, False))
while number_directional_deformations != 3:
    number_directional_deformations =len(solution.GetChildren(DataModelObjectCategory.DirectionalDeformation, False))
    if number_directional_deformations < 3:
        solution.AddDirectionalDeformation()
    if number_directional_deformations > 3:
        solution.Children[number_directional_deformations].Delete()
## Set Directions
deformationX = solution.Children[1]
deformationY = solution.Children[2]
deformationZ = solution.Children[3]

deformationX.NormalOrientation = NormalOrientationType.XAxis
deformationY.NormalOrientation = NormalOrientationType.YAxis
deformationZ.NormalOrientation = NormalOrientationType.ZAxis
"""
number_udr = len(solution.GetChildren(DataModelObjectCategory.UserDefinedResult, False))
if number_udr < 1:
    solution..AddUserDefinedResult()
    udr = solution.Children[number_udr]
    udr.Expression = 'UVECTORS'
##
## Solves the model
Model.Solve()
