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
folder_name = "data_dir_"
## Update Sample Number
for root, dirs, files in os.walk(path+"\\.."):
    for sample_dir in dirs:
        if (folder_name in sample_dir) and (len(folder_name)+1 == len(sample_dir)):
            sample_number += 1

directory = folder_name + sample_number.ToString()
parent_dir = "D:\\Ansys Simulations\\Project\\2D\\v11_test"
path = os.path.join(parent_dir, directory)

## Create log file
log_file = "log.txt"
log_file_path = os.path.join(path + '\\..', log_file)
log_file_created = False
for root, dirs, files in os.walk(path+"\\.."):
    for file in files:
        if log_file in file:
            log_file_created = True
if not(log_file_created):
    f_log= open(log_file_path ,"w+")
    row = ['SAMPLE',"ACTION","PATH"]
    f_log.write("{: <20} {: <20} {: <20}\n".format(*row))
    f_log.close()
    
f_log= open(log_file_path ,"a+")

try:
    os.mkdir(path)
    row = [sample_number.ToString(),"CREATE", path]
    f_log.write("{: <20} {: <20} {: <20}\n".format(*row))
    f_log.close()
except:
    row = [sample_number.ToString(),"OVERWRITE", path]
    f_log.write("{: <20} {: <20} {: <20}\n".format(*row))
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

## Export Named Selections
for  i, ns in enumerate(Model.NamedSelections.Children):
    filename = "named_selection_test_"+ (i+1).ToString() +".txt"
    file_path = os.path.join(path, filename)
    ns.ExportToTextFile(file_path)
    
