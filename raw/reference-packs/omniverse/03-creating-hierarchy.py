# Activity 3: Creating a Hierarchy
from pxr import Usd, UsdGeom
from utils import create_new_stage
from utils.visualization import DisplayUSD

file_path = 'assets/03-second-stage.usda'

# in this example, Geometry is the root prim. We are also defining three types of prims here: scope, xform, and cube.
# Geometry
#   - GroupTransform
#      - Cube
#
# Xform defines a transform (translate, rotation, scale).
# Scope is a simple container that does not hold transform data.
# Cube defines a primitive rectilinear cube.

stage: Usd.Stage = create_new_stage(file_path)

# define a `Scope` Prim in stage at `/Geometry`:
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage , "/Geometry")

# define an `Xform` Prim in stage as a child of `geom_scope` called `GroupTransform`:
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))

# define a `Cube` in the stage as a child of `xform`, called `Box`:
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

stage.Save()
#DisplayUSD(file_path, show_usd_code=True)