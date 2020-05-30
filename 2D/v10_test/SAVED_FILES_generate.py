import os

## Creates solutions and exports them

## Load-in the body
part = Model.Geometry.Children[0] #Get first "geometry"
body = part.Children[0] #Get  first body
geobody = body.GetGeoBody()
#selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)  # Create an empty selection.

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

## Create log file
log_file = "log.txt"
log_file_path = os.path.join(path + '\\..', log_file)
f_log= open(log_file_path ,"w+")

row = ['SAMPLE',"ACTION","PATH"]
f_log.write("{: <20} {: <20} {: <20}\n".format(*row))
f_log.close()
f_log= open(log_file_path ,"a+")

try:
    os.mkdir(path)
    row = [sample_number.ToString(),"CREATE", path]
    f_log.write("{: <20} {: <20} {: <20}".format(*row))
    f_log.close()
except:
    row = [sample_number.ToString(),"OVERWRITE", path]
    f_log.write("{: <20} {: <20} {: <20}".format(*row))
    f_log.close()

##Create files in this directory to store displacements and forces
filename = "disp_test_"+ sample_number.ToString() +".txt"
file_path = os.path.join(path, filename)
f_disp= open(file_path ,"w+")

filename = "force_test_"+ sample_number.ToString() +".txt"
file_path = os.path.join(path, filename)
f_force= open(file_path ,"w+")

##Create List With relevant Boundary Conditions
boundary_conditions = []
for item in analysis.GetChildren(DataModelObjectCategory.NodalDisplacement, False):
    boundary_conditions.append(item)
for item in analysis.GetChildren(DataModelObjectCategory.NodalForce, False):
    boundary_conditions.append(item)

##Write BCs in file
for bc in boundary_conditions:
    x = bc.XComponent.Output.DiscreteValues[0].Value
    y = bc.YComponent.Output.DiscreteValues[0].Value
    z = bc.ZComponent.Output.DiscreteValues[0].Value
    unit = bc.XComponent.Output.DiscreteValues[0].Unit
    if bc.DataModelObjectCategory == DataModelObjectCategory.NodalDisplacement:
        line = bc.Location.Name +"\t" + "["+unit+"]" +"\t" + x.ToString()+"\t" + y.ToString()+"\t" + z.ToString()
        f_disp.write( line + "\n")
    if bc.DataModelObjectCategory == DataModelObjectCategory.NodalForce:
        line = bc.Location.Name +"\t" + "["+unit+"]" +"\t" + x.ToString()+"\t" + y.ToString()+"\t" + z.ToString()
        f_force.write( line + "\n")
## Close files
f_disp.close() 
f_force.close()

## Export Solution to another file
filename = "solutions_test_"+ sample_number.ToString() +".txt"
file_path = os.path.join(path, filename)
udr.ExportToTextFile(file_path)

