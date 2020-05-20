# encoding: utf-8
# 2020 R1
SetScriptVersion(Version="20.1.164")
system1 = GetSystem(Name="SYS")
model1 = system1.GetContainer(ComponentName="Model")
simulationMeshProperties1 = model1.GetMeshProperties()
simulationMeshProperties1.saveMeshFileInSeparateFile = True
