import os

## Creates solutions and exports them

## Load-in the body
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0] #Get  first body
geobody = body.GetGeoBody()
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.


## Delete previously assigned forces
analysis = Model.Analyses[0]
solution = analysis.Solution

number_udr = len(solution.GetChildren(DataModelObjectCategory.UserDefinedResult, False))
if number_udr < 1:
    solution.AddUserDefinedResult()
number_udr = len(solution.GetChildren(DataModelObjectCategory.UserDefinedResult, False))
udr = solution.Children[number_udr]
udr.Expression = 'UVECTORS'
##
"""
nodal.XComponent.Output.DiscreteValues[0].Value

"""

## Solves the model
Model.Solve()

## Create folders to store solutions
sample_number=1
directory = "test_data_dir_" + sample_number.ToString()
parent_dir = "D:\\Ansys Simulations\\Project\\2D\\v10_test"
path = os.path.join(parent_dir, directory)
try:
    os.mkdir(path)
except:
    pass

##Create files in this directory to store displacements and forces
filename = "test_"+ sample_number.ToString() +".txt"
file_path = os.path.join(path, filename)
f= open(file_path ,"w+")

