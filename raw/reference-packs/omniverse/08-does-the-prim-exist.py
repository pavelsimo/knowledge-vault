# Activity 8: Does the Prim Exist?
from pxr import Usd

file_path = "assets/03-second-stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim
if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")