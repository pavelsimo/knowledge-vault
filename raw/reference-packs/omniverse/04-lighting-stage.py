# Activity 4: Lighting a Stage
from math import pi
from pxr import Gf, Usd, UsdGeom, UsdLux
from utils.visualization import DisplayUSD

file_path = 'assets/03-second-stage.usda'
stage: Usd.Stage = Usd.Stage.Open(file_path)
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath("GroupTransform"))
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath("Box"))

# define a `Scope` Prim in stage at `/Lights`:
lights_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Lights")

# define a `Sun` prim in stage as a child of `lights_scope`, called `Sun`:
distant_light = UsdLux.DistantLight.Define(stage, lights_scope.GetPath().AppendPath("Sun"))

# define a `SphereLight` prim in stage as a child of lights_scope called `SphereLight`:
sphere_light = UsdLux.SphereLight.Define(stage, lights_scope.GetPath().AppendPath("SphereLight"))

# configure the distant light's emissive attributes:
distant_light.GetColorAttr().Set(Gf.Vec3f(1.0, 0.0, 0.0)) # Light color (red)
distant_light.GetIntensityAttr().Set(120.0) # Light intensity

# position the distant light in the 3D scene:
distant_light_transform = distant_light.GetTransformOp()

if not distant_light_transform:
    distant_light_transform = distant_light.AddTransformOp()

distant_light_transform.Set(Gf.Matrix4d((pi/4, 0, -pi/4, 0), (0, 1, 0, 0), (pi/4, 0, pi/4, 0), (10, 0, 10, 1)))
distant_light.GetXformOpOrderAttr().Set([distant_light_transform.GetName()])

# configure the sphere light's emissive attributes:
sphere_light.GetColorAttr().Set(Gf.Vec3f(0.0, 0.0, 1.0)) # light color (blue)
sphere_light.GetIntensityAttr().Set(50000.0) # light intensity

# position the sphere light in the 3D scene:
sphere_light_transform = sphere_light.GetTransformOp()
if not sphere_light_transform:
    sphere_light_transform = sphere_light.AddTransformOp()
sphere_light_transform.Set(Gf.Matrix4d((pi/4, 0, pi/4, 0), (0, 1, 0, 0), (-pi/4, 0, pi/4, 0), (-10, 0, 10, 1)))
sphere_light.GetXformOpOrderAttr().Set([sphere_light_transform.GetName()])

stage.Save()
#DisplayUSD(file_path, show_usd_code=True, show_usd_lights=True)