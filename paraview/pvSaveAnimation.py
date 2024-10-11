# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
import os
import pathlib as pl
import sys

# set parameters based on material input
if len(sys.argv) != 2 or sys.argv[1] not in ['abs', 'pekk']:
    print("Usage: pvpython pvSaveAnimation.py [abs|pekk]")
    sys.exit()
    
material = sys.argv[1]

if material == 'abs':
    matDiff = 9e-08
    tempScale_low = 373.15
    tempScale_up = 528.15
elif material == 'pekk':
    matDiff = 1.99e-7
    tempScale_low = 433.15
    tempScale_up = 629.15

# Get current working directory
cwd = os.getcwd()   # "data" directory
pathTo_pv_ch_pvd = pl.Path(cwd) / 'paraview_ch.pvd'
pathTo_pv_marker_pvd = pl.Path(cwd) / 'paraview_marker.pvd'

# create enums for the directories
map_dir = { 0: 'temperature', 1: 'voxel', 2: 'octree'}

# Create directories at the level of the "data" directory, i.e. at the level of the "runs" directory
dirs = [ map_dir[i] for i in range(3)]
for d in dirs:
    dir_path = pl.Path(cwd).parent.joinpath(d)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
# for d in dirs:
#     pl.Path(cwd).parent.joinpath(d).mkdir(parents=True, exist_ok=True)
    
# Create dictionary of paths to the directories
pathToDirs = {d: pl.Path(cwd).parent.joinpath(d) for d in dirs}

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'PVD Reader'
paraview_chpvd = PVDReader(registrationName='paraview_ch.pvd', FileName=str(pathTo_pv_ch_pvd))
paraview_chpvd.CellArrays = ['k', 'rank']

paraview_markerpvd = PVDReader(registrationName='paraview_marker.pvd', FileName= str(pathTo_pv_marker_pvd))
paraview_markerpvd.CellArrays = ['rank']
paraview_markerpvd.PointArrays = ['k']

# update animation scene based on data timesteps
animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Get the time keeper and time steps
timeKeeper = GetTimeKeeper()
time_steps = timeKeeper.TimestepValues
numFrames = len(time_steps)
print("Total number of frames: {0}".format(numFrames))

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
Show(paraview_chpvd, renderView1, 'UnstructuredGridRepresentation')
Show(paraview_markerpvd, renderView1, 'UnstructuredGridRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# set active source
# SetActiveSource(paraview_chpvd)

# set active source
# SetActiveSource(paraview_markerpvd)

# create a new 'Append Attributes'
appendAttributes1 = AppendAttributes(registrationName='AppendAttributes1', Input=[paraview_chpvd, paraview_markerpvd])

# show data in view
Show(appendAttributes1, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(paraview_markerpvd, renderView1)
Hide(paraview_chpvd, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=appendAttributes1)
threshold1.Scalars = ['CELLS', 'k']
threshold1.ThresholdRange = [matDiff, matDiff]

# show data in view
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(appendAttributes1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(threshold1Display, ('POINTS', 'k'))

# rescale color and/or opacity maps used to include current data range
threshold1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
# threshold1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'k'
kLUT = GetColorTransferFunction('k')
kLUT.RescaleTransferFunction(tempScale_low, tempScale_up)

# get opacity transfer function/opacity map for 'k'
kPWF = GetOpacityTransferFunction('k')
kPWF.RescaleTransferFunction(tempScale_low, tempScale_up)

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# hide color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, False)

# Set the layout size for rendering
layout1 = GetLayout()
layout1.SetSize([2046, 2046])
layout1.PreviewMode = [2048, 2048]

animationScene1.GoToLast()

# current camera placement for renderView1
renderView1.CameraPosition = [0.11074966357080558, -0.021912925896228903, 0.1262262240511014]
renderView1.CameraFocalPoint = [0.009577158535611967, 0.036499047120428875, 0.009402278017785835]
renderView1.CameraViewUp = [-0.6123724356957945, 0.3535533905932737, 0.7071067811865477]
renderView1.CameraParallelScale = 0.03533928265994693
renderView1.CameraParallelProjection = 1

# saveScreenshot( str(pathToDirs[map_dir[0]] / 'image.png'), 
#                 renderView1, 
#                 ImageResolution=[2046, 2046], 
#                 OverrideColorPalette='WhiteBackground', 
#                 CompressionLevel='1')

# Save Temperature Animation
SaveAnimation(  str(pathToDirs[map_dir[0]] / 'image.png'), 
                renderView1, ImageResolution=[2046, 2046],
                OverrideColorPalette='WhiteBackground',
                FrameWindow=[0, numFrames-1], 
                CompressionLevel='1')