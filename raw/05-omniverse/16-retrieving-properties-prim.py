# Activity 17: Retrieving Properties of a Prim
# Properties are the other kind of namespace object in OpenUSD. Whereas prims provide the organization and indexing for a composed scene, properties contain the "real data".
#
# There are two types of properties: attributes and relationships.
#
# To retrieve the properties of a prim, we would use the GetProperties method. For this demonstration we will be using GetPropertyNames()
# instead to retrieve the names of the properties. This will not grab the properties themselves, but a list of the names of the properties. Use GetProperties to retrieve the properties themselves.

from pxr import Usd, UsdGeom, Gf
from utils.visualization import DisplayUSD
from utils.helperfunctions import create_new_stage

file_path = "assets/06-attributes.usda"

#stage: Usd.Stage = Usd.Stage.Open(file_path)
stage: Usd.Stage = create_new_stage(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim())

# Define a sphere under the World xForm:
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, world_xform.GetPath().AppendPath("Sphere"))

# Define a cube under the World xForm and set it to be 5 units away from the sphere:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))

# Get the property names of the cube prim:
cube_prop_names = cube.GetPrim().GetPropertyNames()

# Print the property names:
for prop_name in cube_prop_names:
    print(prop_name)

stage.Save()
#DisplayUSD(file_path, show_usd_code=True)