# Activity 11: Getting, Validating, and Setting Prims at Path
# Each prim has a path to describe its location in namespace.
# For example, we defined a prim hello at path /hello and another prim world at path /hello/world.
# We can retrieve prims using their path using GetPrimAtPath(). This will either return a valid or invalid prim. When using GetPrimAtPath() we should always check if the returned prim is valid before using it.
# To check if a prim is valid we can use the IsValid() method. Valid means that the prim exists in the stage. Invalid is when the prim does not exist in the stage or when the path is invalid.
#
# https://openusd.org/release/glossary.html#usdglossary-path
# https://openusd.org/release/glossary.html#usdglossary-namespace
from pxr import Usd

stage: Usd.Stage = Usd.Stage.Open("assets/04-prims.usda")

# Get the primitive at the path "/hello" from the current stage
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")

# Get the primitive at the path "/world" from the current stage
# Note: This will return an invalid prim because "/world" does not exist, but if changed to "/hello/world" it will return a valid prim
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

print(hello_prim.IsValid())
print(world_prim.IsValid())
stage.Save()
