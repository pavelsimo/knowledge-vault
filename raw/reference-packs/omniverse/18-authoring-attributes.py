# Activity 19: Authoring Attributes
# In the last activity, we used the Get() method to retrieve the value of the attribute. To set the values, we use the Set() method.
#
# Here is an example of setting a value to the radius attribute.
#
# sphere_prim.GetRadiusAttr().Set(100.0)
# When ran, it will modify the above .usd as:
#
# def Sphere "Sphere"{
#     double radius = 100
# }
# Based on our last modification, if we were to use Get() it would return 100.
#
# When getting attribute values, USD will apply value resolution, since we authored a default value. The Get() method will retrieve the value of the attribute.
# To set the values, we use the Set() method. This will resolve to the authored value rather than the fallback value from the sphere schema.

from pxr import Usd, UsdGeom, Gf
#from utils.visualization import DisplayUSD

file_path = "assets/06-attributes.usda"
stage: Usd.Stage = Usd.Stage.Open(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())

sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5,0,0))

# Get the size, display color, and extent attributes of the sphere
cube_size: Usd.Attribute = cube.GetSizeAttr()
cube_displaycolor: Usd.Attribute = cube.GetDisplayColorAttr()
cube_extent: Usd.Attribute = cube.GetExtentAttr()

# Modify the radius, extent, and display color attributes:
cube_size.Set(cube_size.Get() * 2)
cube_extent.Set(cube_extent.Get() * 2)
cube_displaycolor.Set([(0.0, 1.0, 0.0)])

stage.Save()
#DisplayUSD(file_path, show_usd_code=True)