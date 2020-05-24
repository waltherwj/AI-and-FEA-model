if not IsProjectUpToDate():
    print("not upt to date")
    DSscript = open("D:/Ansys Simulations/Project/2D/v6_test/MESH_error_handling.py", "r")
    DSscriptcommand=DSscript.read()
    model1.SendCommand(Command=DSscriptcommand,Language="Python")