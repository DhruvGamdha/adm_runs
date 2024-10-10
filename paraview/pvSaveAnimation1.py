# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
import os
import pathlib as pl
import sys

# set parameters based on material input
if len(sys.argv) != 2 and sys.argv[1] not in ['abs', 'pekk']:
    print("Please provide material as input")
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
    pl.Path(cwd).parent.joinpath(d).mkdir(parents=True, exist_ok=True)
    
# Create dictionary of paths to the directories
pathToDirs = {d: pl.Path(cwd).parent.joinpath(d) for d in dirs}

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'PVD Reader'
# paraview_chpvd = PVDReader(registrationName='paraview_ch.pvd', FileName='/run/user/1000/gvfs/sftp:host=frontera/scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_004/data/paraview_ch.pvd')
paraview_chpvd = PVDReader(registrationName='paraview_ch.pvd', FileName=str(pathTo_pv_ch_pvd))
paraview_chpvd.CellArrays = ['k', 'rank']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Get the total number of frames for save animation
numFrames = animationScene1.EndTime
print(f"Total number of frames: {numFrames}")

# create a new 'PVD Reader'
# paraview_markerpvd = PVDReader(registrationName='paraview_marker.pvd', FileName='/run/user/1000/gvfs/sftp:host=frontera/scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_004/data/paraview_marker.pvd')
paraview_markerpvd = PVDReader(registrationName='paraview_marker.pvd', FileName= str(pathTo_pv_marker_pvd))
paraview_markerpvd.CellArrays = ['rank']
paraview_markerpvd.PointArrays = ['k']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
paraview_chpvdDisplay = Show(paraview_chpvd, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
paraview_chpvdDisplay.Representation = 'Surface'
paraview_chpvdDisplay.ColorArrayName = [None, '']
paraview_chpvdDisplay.PointSize = 10.0
paraview_chpvdDisplay.SelectTCoordArray = 'None'
paraview_chpvdDisplay.SelectNormalArray = 'None'
paraview_chpvdDisplay.SelectTangentArray = 'None'
paraview_chpvdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
paraview_chpvdDisplay.SelectOrientationVectors = 'None'
paraview_chpvdDisplay.ScaleFactor = 0.006083000078797341
paraview_chpvdDisplay.SelectScaleArray = 'None'
paraview_chpvdDisplay.GlyphType = 'Arrow'
paraview_chpvdDisplay.GlyphTableIndexArray = 'None'
paraview_chpvdDisplay.GaussianRadius = 0.00030415000393986703
paraview_chpvdDisplay.SetScaleArray = [None, '']
paraview_chpvdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
paraview_chpvdDisplay.OpacityArray = [None, '']
paraview_chpvdDisplay.OpacityTransferFunction = 'PiecewiseFunction'
paraview_chpvdDisplay.DataAxesGrid = 'GridAxesRepresentation'
paraview_chpvdDisplay.PolarAxes = 'PolarAxesRepresentation'
paraview_chpvdDisplay.ScalarOpacityUnitDistance = 0.004474471391234536
paraview_chpvdDisplay.OpacityArrayName = ['CELLS', 'k']

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show data in view
paraview_markerpvdDisplay = Show(paraview_markerpvd, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
paraview_markerpvdDisplay.Representation = 'Surface'
paraview_markerpvdDisplay.ColorArrayName = [None, '']
paraview_markerpvdDisplay.PointSize = 10.0
paraview_markerpvdDisplay.SelectTCoordArray = 'None'
paraview_markerpvdDisplay.SelectNormalArray = 'None'
paraview_markerpvdDisplay.SelectTangentArray = 'None'
paraview_markerpvdDisplay.OSPRayScaleArray = 'k'
paraview_markerpvdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
paraview_markerpvdDisplay.SelectOrientationVectors = 'None'
paraview_markerpvdDisplay.ScaleFactor = 0.006083000078797341
paraview_markerpvdDisplay.SelectScaleArray = 'None'
paraview_markerpvdDisplay.GlyphType = 'Arrow'
paraview_markerpvdDisplay.GlyphTableIndexArray = 'None'
paraview_markerpvdDisplay.GaussianRadius = 0.00030415000393986703
paraview_markerpvdDisplay.SetScaleArray = ['POINTS', 'k']
paraview_markerpvdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
paraview_markerpvdDisplay.OpacityArray = ['POINTS', 'k']
paraview_markerpvdDisplay.OpacityTransferFunction = 'PiecewiseFunction'
paraview_markerpvdDisplay.DataAxesGrid = 'GridAxesRepresentation'
paraview_markerpvdDisplay.PolarAxes = 'PolarAxesRepresentation'
paraview_markerpvdDisplay.ScalarOpacityUnitDistance = 0.004474471391234536
paraview_markerpvdDisplay.OpacityArrayName = ['POINTS', 'k']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
paraview_markerpvdDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
paraview_markerpvdDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(paraview_chpvd)

# set active source
SetActiveSource(paraview_markerpvd)

# create a new 'Append Attributes'
appendAttributes1 = AppendAttributes(registrationName='AppendAttributes1', Input=[paraview_chpvd, paraview_markerpvd])

# show data in view
appendAttributes1Display = Show(appendAttributes1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
appendAttributes1Display.Representation = 'Surface'
appendAttributes1Display.ColorArrayName = [None, '']
appendAttributes1Display.PointSize = 10.0
appendAttributes1Display.SelectTCoordArray = 'None'
appendAttributes1Display.SelectNormalArray = 'None'
appendAttributes1Display.SelectTangentArray = 'None'
appendAttributes1Display.OSPRayScaleArray = 'k'
appendAttributes1Display.OSPRayScaleFunction = 'PiecewiseFunction'
appendAttributes1Display.SelectOrientationVectors = 'None'
appendAttributes1Display.ScaleFactor = 0.006083000078797341
appendAttributes1Display.SelectScaleArray = 'None'
appendAttributes1Display.GlyphType = 'Arrow'
appendAttributes1Display.GlyphTableIndexArray = 'None'
appendAttributes1Display.GaussianRadius = 0.00030415000393986703
appendAttributes1Display.SetScaleArray = ['POINTS', 'k']
appendAttributes1Display.ScaleTransferFunction = 'PiecewiseFunction'
appendAttributes1Display.OpacityArray = ['POINTS', 'k']
appendAttributes1Display.OpacityTransferFunction = 'PiecewiseFunction'
appendAttributes1Display.DataAxesGrid = 'GridAxesRepresentation'
appendAttributes1Display.PolarAxes = 'PolarAxesRepresentation'
appendAttributes1Display.ScalarOpacityUnitDistance = 0.004474471391234536
appendAttributes1Display.OpacityArrayName = ['POINTS', 'k']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
appendAttributes1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
appendAttributes1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# hide data in view
Hide(paraview_markerpvd, renderView1)

# hide data in view
Hide(paraview_chpvd, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=appendAttributes1)
threshold1.Scalars = ['POINTS', 'k']
threshold1.ThresholdRange = [0.0, 488.17011821722383]

# Properties modified on threshold1
threshold1.Scalars = ['CELLS', 'k']
threshold1.ThresholdRange = [matDiff, matDiff]

# show data in view
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
threshold1Display.Representation = 'Surface'
threshold1Display.ColorArrayName = [None, '']
threshold1Display.PointSize = 10.0
threshold1Display.SelectTCoordArray = 'None'
threshold1Display.SelectNormalArray = 'None'
threshold1Display.SelectTangentArray = 'None'
threshold1Display.OSPRayScaleArray = 'k'
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.SelectOrientationVectors = 'None'
threshold1Display.ScaleFactor = 0.004087015800178051
threshold1Display.SelectScaleArray = 'None'
threshold1Display.GlyphType = 'Arrow'
threshold1Display.GlyphTableIndexArray = 'None'
threshold1Display.GaussianRadius = 0.00020435079000890254
threshold1Display.SetScaleArray = ['POINTS', 'k']
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityArray = ['POINTS', 'k']
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1Display.ScalarOpacityUnitDistance = 0.006591422133758108
threshold1Display.OpacityArrayName = ['POINTS', 'k']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
threshold1Display.ScaleTransferFunction.Points = [371.05679032971295, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
threshold1Display.OpacityTransferFunction.Points = [371.05679032971295, 0.0, 0.5, 0.0, 488.17011821722383, 1.0, 0.5, 0.0]

# hide data in view
Hide(appendAttributes1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(threshold1Display, ('POINTS', 'k'))

# rescale color and/or opacity maps used to include current data range
threshold1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'k'
kLUT = GetColorTransferFunction('k')

# get opacity transfer function/opacity map for 'k'
kPWF = GetOpacityTransferFunction('k')

# Rescale transfer function
kLUT.RescaleTransferFunction(tempScale_low, tempScale_up)

# Rescale transfer function
kPWF.RescaleTransferFunction(tempScale_low, tempScale_up)

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# hide color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, False)

# get layout
layout1 = GetLayout()

#Enter preview mode
layout1.PreviewMode = [2048, 2048]

animationScene1.GoToLast()

# layout/tab size in pixels
layout1.SetSize(2046, 2046)

# current camera placement for renderView1
renderView1.CameraPosition = [0.11074966357080558, -0.021912925896228903, 0.1262262240511014]
renderView1.CameraFocalPoint = [0.009577158535611967, 0.036499047120428875, 0.009402278017785835]
renderView1.CameraViewUp = [-0.6123724356957945, 0.3535533905932737, 0.7071067811865477]
renderView1.CameraParallelScale = 0.03533928265994693
renderView1.CameraParallelProjection = 1

# # save screenshot
# SaveScreenshot('/media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/test_img.png', layout1, ImageResolution=[2048, 2048],
#     OverrideColorPalette='WhiteBackground', 
#     # PNG options
#     CompressionLevel='1')


# saveScreenshot( str(pathToDirs[map_dir[0]] / 'image.png'), 
#                 layout1, 
#                 ImageResolution=[2046, 2046], 
#                 OverrideColorPalette='WhiteBackground', 
#                 CompressionLevel='1')

# save animation
# SaveAnimation('/media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/test_img2/image.png', layout1, ImageResolution=[2046, 2046],
#     OverrideColorPalette='WhiteBackground',
#     FrameWindow=[0, 84], 
#     # PNG options
#     CompressionLevel='1')

# Save Temperature Animation
SaveAnimation(  str(pathToDirs[map_dir[0]] / 'image.png'), 
                layout1, ImageResolution=[2046, 2046],
                OverrideColorPalette='WhiteBackground',
                FrameWindow=[0, numFrames], 
                CompressionLevel='1')

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(2046, 2046)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.11074966357080558, -0.021912925896228903, 0.1262262240511014]
renderView1.CameraFocalPoint = [0.009577158535611967, 0.036499047120428875, 0.009402278017785835]
renderView1.CameraViewUp = [-0.6123724356957945, 0.3535533905932737, 0.7071067811865477]
renderView1.CameraParallelScale = 0.03533928265994693
renderView1.CameraParallelProjection = 1

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).