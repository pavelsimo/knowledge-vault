# Activity 5: Adding Attributes to a Prim

# Attributes are the most common type of property authored in most USD scenes.
# An attribute consist of a type and default value. It can also include time sampled values.
from pxr import Usd, UsdGeom

file_path = 'assets/03-second-stage.usda'
stage: Usd.Stage = Usd.Stage.Open(file_path)

# get the Cube prim at path: `/Geometry/GroupTransform/Box`:
cube: UsdGeom.Cube = UsdGeom.Cube(stage.GetPrimAtPath("/Geometry/GroupTransform/Box"))

# get all attribute names associated with Cube:
cube_attrs = cube.GetSchemaAttributeNames()

# print out all the attribute names for Cube:
for attr in cube_attrs:
    print(attr)

# get the Attribute for "Display Color":
cube_color_attr: Usd.Attribute = cube.GetDisplayColorAttr()

# set the "Display Color" attribute to red:
cube_color_attr.Set([(1.0, 0.0, 0.0)])

stage.Save()