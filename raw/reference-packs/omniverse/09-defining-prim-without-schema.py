# Activity 10: Defining a Prim Without a Schema

# a prim is the primary container object in usd. it can contain other prims and properties holding data.
# to create a generate prim on the stage we use DefinePrim(). these are prims that do not have any schema to dictate what kind of data the prim contains.
# when creating a cube, lights, meshes, etc, we should use the appropriate schema api.
#
# https://openusd.org/release/api/class_usd_stage.html#a6151ae804f7145e451d9aafdde347730
#
from utils.helperfunctions import create_new_stage
from pxr import Usd

stage: Usd.Stage = create_new_stage("assets/04-prims.usda")

# define a new primitive at the path "/hello" on the current stage:
stage.DefinePrim("/hello")

# define a new primitive at the path "/hello/world" on the current stage:
stage.DefinePrim("/hello/world")

stage.Save()
print(stage.ExportToString())