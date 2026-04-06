# Activity 18: Retrieving Properties of a Prim
# Attributes are the most common type of property authored in most USD scenes.
#
# An example of a simple attribute that describes the radius of a sphere:
#
# def Sphere "Sphere"{
#     double radius = 10
# }
# We interact with attributes through the UsdAttribute API.
#
# Since our sphere is of type UsdGeom.Sphere, we can use the schema-specific API to get and set the radius attribute.
#
# GetRadiusAttr() will return a UsdAttribute object that can be used to modify the attribute. Which means it will not retrieve the value of the attribute. To get the value of an attribute, use the Get() method.
#
# For example, to get the value of the radius attribute, we would use the following snippet.
#
# sphere_prim.GetRadiusAttr().Get()
# Let's use the Get() method for the Radius, Display Color, and Extent Attributes.
#
# Since we have not explicitly authored any attribute values, Get() will return the fallback value that was defined in the schema.
from pxr import Usd, UsdGeom, Gf
from utils.visualization import DisplayUSD

file_path = "assets/06-attributes.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the attributes of the cube prim
cube_attrs = cube.GetPrim().GetAttributes()
for attr in cube_attrs:
    print(attr)

# Get the size, display color, and extent attributes of the cube
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

print(f"Size: {cube_size.Get()}")
print(f"Display Color: {cube_displaycolor.Get()}")
print(f"Extent: {cube_extent.Get()}")

stage.Save()
#DisplayUSD(file_path, show_usd_code=True)