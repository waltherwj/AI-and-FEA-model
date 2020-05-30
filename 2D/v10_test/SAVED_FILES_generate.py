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
sample_number=2
directory = "test_data_dir_" + sample_number.ToString()
parent_dir = "D:\\Ansys Simulations\\Project\\2D\\v10_test"
path = os.path.join(parent_dir, directory)
try:
    os.mkdir(path)
except:
    log_file = "log.txt"
    log_file_path = os.path.join(path + '\\..', log_file)
    f_log= open(log_file_path ,"w+")
    f_log.write("Folder for sample # " + sample_number.ToString() + " already exists -- OVERWRITING")
    f_log.close()

##Create files in this directory to store displacements and forces
filename = "test_"+ sample_number.ToString() +".txt"
file_path = os.path.join(path, filename)
f= open(file_path ,"w+")

##Write in file
for i in range(10):
     f.write("This is line %d\r\n" % (i+2))
     
## Close file
f.close() 

