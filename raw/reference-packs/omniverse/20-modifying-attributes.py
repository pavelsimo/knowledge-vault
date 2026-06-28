# Activity 21: Modifying Attributes
# After creating an attribute, we can set and get the value of the attribute, similar to what we did in the previous activity.
#
# Add the following code to the cell below, then run the cell:
#
# # Defining the weight attribute
# box_weight_attr: Usd.Attribute = box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float, custom=True)
# # Set the value of the weight attribute
# box_weight_attr.Set(50)
#
# # Print the weight of the box
# print("Weight of Box:", box_weight_attr.Get())
# Try applying the same logic to the other attributes.

from pxr import Usd, UsdGeom, Sdf
from utils.helperfunctions import create_new_stage
#from utils.visualization import DisplayUSD

file_path = "assets/07-custom_attributes.usda"

stage: Usd.Stage = Usd.Stage.Open(file_path)


world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
geometry_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, world_xform.GetPath().AppendPath("Geometry"))

box_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geometry_xform.GetPath().AppendPath("Box"))
box_prim: Usd.Prim = box_xform.GetPrim()
box_prim.GetReferences().AddReference("assets/08-cubebox_a02_distilled.usd")

box_prim.CreateAttribute("size_cm", Sdf.ValueTypeNames.Float, custom=True)
box_prim.CreateAttribute("type", Sdf.ValueTypeNames.String, custom=True)
box_prim.CreateAttribute("hazardous_material", Sdf.ValueTypeNames.Bool, custom=True)

# Defining the weight attribute
box_weight_attr: Usd.Attribute = box_prim.CreateAttribute("weight_lb", Sdf.ValueTypeNames.Float, custom=True)
# Set the value of the weight attribute
box_weight_attr.Set(50)

# Print the weight of the box
print("Weight of Box:", box_weight_attr.Get())

stage.Save()
#DisplayUSD(file_path, show_usd_code=True)