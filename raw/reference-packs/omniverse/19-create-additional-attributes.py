# Activity 20: Creating Additional Attributes
# For custom attributes that are not apart of any schema, we use the CreateAttribute() method.
#
# Custom attributes in OpenUSD are used to define additional, user-specific properties for objects within a 3D scene. These attributes extend beyond
# the standard properties like position, rotation, and color, allowing creators to add unique data relevant to their specific needs. For example,
# custom attributes can store information such as material properties, animation controls, or metadata for a particular workflow.
#
# When creating an attribute in OpenUSD, we need to specify the type of the attribute. For example, we can create a float attribute for the weight of the box:
#
# box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float)
# ValueTypeNames represent an attribute's type. These are defined in Sdf and more types can be found in OpenUSD's

from pxr import Usd, UsdGeom, Gf
#from utils.visualization import DisplayUSD

from pxr import Usd, UsdGeom, Sdf
from utils.helperfunctions import create_new_stage
#from utils.visualization import DisplayUSD

file_path = "assets/07-custom_attributes.usda"
stage: Usd.Stage = create_new_stage(file_path)

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("assets/08-cubebox_a02_distilled.usd")

# Create additional attributes for the box prim
box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("size_cm", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("type", Sdf.ValueTypeNames.String, custom=True)
box_prim.CreateAttribute("hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Save the stage
stage.Save()
#DisplayUSD(file_path, show_usd_code=True)