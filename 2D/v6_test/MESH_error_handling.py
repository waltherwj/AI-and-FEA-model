
try:
    DSscript = open("D:/Ansys Simulations/Project/2D/v6_test/MESH_generate.py", "r")
    DSscriptcommand=DSscript.read()
    model1.SendCommand(Command=DSscriptcommand,Language="Python")
except:
    mesh_method.Method = MethodType.Automatic
    Model.Mesh.GenerateMesh()
