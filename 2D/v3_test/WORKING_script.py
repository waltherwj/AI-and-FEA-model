# encoding: utf-8
# 2020 R1
SetScriptVersion(Version="20.1.164")
system1 = GetSystem(Name="SYS")
geometry1 = system1.GetContainer(ComponentName="Geometry")
DSscript = open("D:/Ansys Simulations/Project/2D/v3_test/generate_random_triangular_element.py", "r")
DSscriptcommand=DSscript.read()
geometry1.SendCommand(Command=DSscriptcommand,Language="Python")
geometry1.Edit(IsSpaceClaimGeometry=True)
#geometry1.Exit()
