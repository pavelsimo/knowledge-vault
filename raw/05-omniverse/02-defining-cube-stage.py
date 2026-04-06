# Activity 2: Defining a Cube in the Stage
from pxr import Usd, UsdGeom
from utils.visualization import DisplayUSD

file_path = 'assets/01-first_stage.usda'

# notice that we're using Usd.Stage.Open() rather than Usd.Stage.CreateNew(), this is because we already created the .usda file.
stage: Usd.Stage = Usd.Stage.Open(file_path)
print(stage.ExportToString())

#DisplayUSD(file_path, show_usd_code=True)

