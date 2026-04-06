# Activity 7: Traversing a Stage
from pxr import Usd

file_path = "assets/03-second-stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

# traversing is done depth-first search and can be used to not just go through the whole stage but a branch of the whole tree.
for prim in stage.Traverse():
    print(prim)