# encoding: utf-8
# 2020 R1

## Create Geometry
SetScriptVersion(Version="20.1.164")
system1 = GetSystem(Name="SYS")
geometry1 = system1.GetContainer(ComponentName="Geometry")
DSscript = open("D:/Ansys Simulations/Project/2D/v11_test/GEOMETRY_generate.py", "r")
DSscriptcommand=DSscript.read()
geometry1.SendCommand(Command=DSscriptcommand,Language="Python")
geometry1.Edit(IsSpaceClaimGeometry=True)
#geometry1.Exit()

## Open Mechanical
modelComponent1 = system1.GetComponent(Name="Model")
modelComponent1.Refresh()
model1 = system1.GetContainer(ComponentName="Model")
model1.Edit()

## Create Mesh
DSscript = open("D:/Ansys Simulations/Project/2D/v11_test/MESH_generate.py", "r")
DSscriptcommand=DSscript.read()
model1.SendCommand(Command=DSscriptcommand,Language="Python")

## Create Named  Selections
DSscript = open("D:/Ansys Simulations/Project/2D/v11_test/NAMED_SELECTIONS_generate.py", "r")
DSscriptcommand=DSscript.read()
model1.SendCommand(Command=DSscriptcommand,Language="Python")

## Create Displacements
DSscript = open("D:/Ansys Simulations/Project/2D/v11_test/DISPLACEMENTS_generate.py", "r")
DSscriptcommand=DSscript.read()
model1.SendCommand(Command=DSscriptcommand,Language="Python")

## Create Loads
DSscript = open("D:/Ansys Simulations/Project/2D/v11_test/LOADS_generate.py", "r")
DSscriptcommand=DSscript.read()
model1.SendCommand(Command=DSscriptcommand,Language="Python")