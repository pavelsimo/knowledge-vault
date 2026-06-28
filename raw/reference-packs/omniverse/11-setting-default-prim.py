# Activity 12: Setting a Default Prim
# SetDefaultPrim() sets the default prim for the stage's root layer.
#
# A Default Prim is metadata on the stage. If the stage's root layer is used as a Reference or Payload it is best practice to set a Default Prim.
#
# https://openusd.org/release/glossary.html#usdglossary-references
# https://openusd.org/release/glossary.html#usdglossary-payload

from pxr import Usd

stage: Usd.Stage = Usd.Stage.Open("assets/04-prims.usda")

stage.DefinePrim("/hello")
stage.DefinePrim("/hello/world")
hello_prim: Usd.Prim = stage.GetPrimAtPath("/hello")
world_prim: Usd.Prim = stage.GetPrimAtPath("/world")

print(hello_prim.IsValid())
print(world_prim.IsValid())

# Set the default primitive of the stage to the primitive at "/hello":
stage.SetDefaultPrim(hello_prim)

stage.Save()
print(stage.ExportToString())