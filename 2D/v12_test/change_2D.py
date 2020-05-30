# encoding: utf-8
# 2020 R1
SetScriptVersion(Version="20.1.164")
system1 = GetSystem(Name="SYS")
geometry1 = system1.GetContainer(ComponentName="Geometry")
geometryProperties1 = geometry1.GetGeometryProperties()
geometryProperties1.GeometryImportAnalysisType = "AnalysisType_2D"
