# Activity 14: Scope and Cube
# Other classes that are a part of UsdGeom are Scope and Cube.
#
# Scope is a grouping primitive and does NOT have transformability. It can be used to organize libraries with large numbers of entry points. It also is best to group actors and environments under partitioning scopes. Besides navigating, it's easy for a user to deactivate all actors or environments by deactivating the root scope.
#
# Cube defines a primitive rectilinear cube centered at the origin.
#
# Similar to how we defined Xform above, we can define Scope and Cube using the same API structure:
#
# UsdGeom.Cube.Define().
# UsdGeom.Scope.Define().
#
# https://openusd.org/release/api/class_usd_geom_cube.html#a77025529a7373c1e74e4f776f282ed8c
# https://openusd.org/release/api/class_usd_geom_scope.html#acdb17fed396719a9a21294ebca0116ae

from pxr import Usd, UsdGeom

stage = Usd.Stage.Open("assets/05-many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

# Define a new Xform primitive at the path "/World/Box" on the current stage:
box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))

# Define a new Scope primitive at the path "/World/Box/Geometry" on the current stage:
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))

# Define a new Cube primitive at the path "/World/Box/Geometry/Cube" on the current stage:
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

stage.Save()