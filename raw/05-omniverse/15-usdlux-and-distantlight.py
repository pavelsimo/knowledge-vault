# Activity 16: UsdLux and DistantLight
# UsdLux is a USD lighting schema that provides a representation for lights.
#
# One of the classes in UsdLux is DistantLight. A light is emitted from a distance source along the -Z axis. This is commonly known as a directional light.
#
# UsdLux is another example of a schema-specific API.
#
# https://openusd.org/release/api/usd_lux_page_front.html
# https://openusd.org/release/api/class_usd_lux_distant_light.html

from pxr import Usd, UsdGeom, UsdShade, UsdLux

stage = Usd.Stage.Open("assets/05-many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# Define a new Scope primitive at the path "/World/Environment" on the current stage:
env: UsdGeom.Scope = UsdGeom.Scope.Define(stage, world.GetPath().AppendPath("Environment"))

# Define a new DistantLight primitive at the path "/World/Environment/SkyLight" on the current stage:
distant_light: UsdLux.DistantLight = UsdLux.DistantLight.Define(stage, env.GetPath().AppendPath("SkyLight"))

# NOTE: The Light will not show up in the scene visually but it is displayed in the hierarchy.

stage.Save()