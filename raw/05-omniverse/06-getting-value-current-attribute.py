# Activity 6: Getting the Value of a Current Attribute

from pxr import Usd, UsdGeom

file_path = "assets/03-second-stage.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

cube: UsdGeom.Cube = UsdGeom.Cube(stage.GetPrimAtPath("/Geometry/GroupTransform/Box"))
cube_color_attr: Usd.Attribute = cube.GetDisplayColorAttr()
cube_color_attr.Set([(1.0, 0.0, 0.0)])

# get the Cube's `size` attribute:
cube_size_attr: Usd.Attribute = cube.GetSizeAttr()

# get the value of the Cube's `Size` attribute, double it and set it as the new value for the `Size` attribute:
cube_size_attr.Set(cube_size_attr.Get() * 2)

# get the prim at the path: `/Geometry/GroupTransform`:
geom_scope: UsdGeom.Scope = stage.GetPrimAtPath("/Geometry/GroupTransform")

# define a Cube Prim in stage as a child of geom_scope called `Small_Box`:
small_box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath("Small_Box"))

# set the position of the `small_box` to x: 4, y: 5, z: 4
UsdGeom.XformCommonAPI(small_box).SetTranslate((4, 5, 4))

stage.Save()