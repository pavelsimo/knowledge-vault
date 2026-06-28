# Activity 15: UsdShade and Material
# UsdShade is a schema for creating and binding materials.
# Material provides a container to store data for defining a "shading material" to a renderer.

from pxr import Usd, UsdGeom, UsdShade

stage = Usd.Stage.Open("assets/05-many_prims.usda")

world: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world.GetPrim())

box: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world.GetPath().AppendPath("Box"))
geo_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Geometry"))
box_geo: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geo_scope.GetPath().AppendPath("Cube"))

# Define a new Scope primitive at the path "/World/Box/Materials" on the current stage:
mat_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, box.GetPath().AppendPath("Materials"))

# Define a new Material primitive at the path "/World/Box/Materials/BoxMat" on the current stage:
box_mat: UsdShade.Material = UsdShade.Material.Define(stage, mat_scope.GetPath().AppendPath("BoxMat"))

# NOTE: The material is not applied to the cube so it will not show up in the scene visually, but it is displayed in the hierarchy.

stage.Save()