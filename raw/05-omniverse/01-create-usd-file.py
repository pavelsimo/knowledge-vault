# Activity 1: Create a USD File
from pxr import Usd, UsdGeom

# - openusd stage refers to a top-level usd file that serves as a container for organizing a hierarchy of elements called prims.
# - stages aren't files, but a unified scenegraph populated from multiple data sources called layers.
# https://openusd.org/release/glossary.html#usdglossary-stage
file_path = 'assets/01-first_stage.usda'

# - creates a new empty USD Stage where 3D scenes are assembled.
# - .usda are human-readable UTF-8 text.
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
print(stage.ExportToString())

# https://openusd.org/release/glossary.html#usdglossary-prim
UsdGeom.Cube.Define(stage, '/cube')
stage.Save()