# encoding: utf-8
# 2020 R1
SetScriptVersion(Version="20.1.164")
system1 = GetSystem(Name="SYS")
# system1.Delete()
# template1 = GetTemplate(
    # TemplateName="Static Structural",
    # Solver="ANSYS")
# system2 = template1.CreateSystem()
# OPEN GEOMETRY
#geometryComponent1 = system2.GetComponent(Name="Geometry")
#geometryComponent1.Update(AllDependencies=True)
geometry1 = system1.GetContainer(ComponentName="Geometry")
geometry1.Edit(IsSpaceClaimGeometry=True)

# LOAD SCRIPT
DSscript = open("D:/Ansys Simulations/Project/2D/v3_test/generate_random_triangular_element.py", "r")
DSscriptcommand=DSscript.read()

#RUN SCRIPT
for i in range(8):
    geometry1.SendCommand(Command=DSscriptcommand,Language="Python")
#geometry1.Edit(IsSpaceClaimGeometry=True)

#Close
#geometry1.Exit()