# Activity 13: UsdGeom and Xform
# UsdGeom defines the 3D graphics-related prim and property schemas that together form a basis for interchanging geometry between Digital Content Creation (DCC) tools in a graphics pipeline.
#
# Some things to know about UsdGeom:
#
# All classes in UsdGeom inherit from UsdGeomImageable, whose intent is to capture any prim type that might want to be rendered or visualized.
# All geometry prims are directly transformable. UsdGeomXformable encapsulates the schema for a prim that is transformable.
# UsdGeomXform is a concrete prim schema for a transform, which is transformable and can scope other child prims.
#
# To define a prim of a specific type we use their API schema. For example, Xform is a class of UsdGeom, so to define a Xform we use UsdGeom.Xform.Define(). DefinePrim() returns a generic UsdPrim and will not include the full schema-specific API available. We will do similar calls for Scope and Cube in the next cells.
#
# https://openusd.org/release/api/usd_geom_page_front.html
# https://openusd.org/release/api/class_usd_geom_xformable.html
# https://openusd.org/release/api/class_usd_geom_xform.html
# https://openusd.org/release/api/class_usd_geom_xform.html#ac91b54ef60ccaabab649fa91a4ece7ae

from pxr import Usd, UsdGeom
from utils.helperfunctions import create_new_stage

# Create a new USD stage with root layer named "many_prims.usda":
stage: Usd.Stage = create_new_stage("assets/05-many_prims.usda")

# Define a new Xform primitive at the path "/World" on the current stage:
world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")

# Set the default primitive of the stage to the "/World" primitive:
stage.SetDefaultPrim(world.GetPrim())

# Save changes to the current stage to its root layer:
stage.Save()
print(stage.ExportToString())