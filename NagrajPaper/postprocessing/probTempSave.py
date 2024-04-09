# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
import sys

material = 'abs'
material_diffusivity = 9e-08
dx=5

if len(sys.argv) == 3:
    material = sys.argv[1]
    dx = float(sys.argv[2])
else:
    print("Please provide the material (abs or pekk) and element dx size as an argument")
    print("<material (abs or pekk)> <voxel dx>")
    sys.exit(1)

if material == 'abs':
    material_diffusivity = 9e-08
elif material == 'pekk':
    material_diffusivity = 1.99e-07

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'PVD Reader'
paraview_chpvd = PVDReader(registrationName='paraview_ch.pvd', FileName='paraview_ch.pvd')
paraview_chpvd.CellArrays = ['k', 'rank']

# create a new 'PVD Reader'
paraview_markerpvd = PVDReader(registrationName='paraview_marker.pvd', FileName='paraview_marker.pvd')
paraview_markerpvd.CellArrays = ['rank']
paraview_markerpvd.PointArrays = ['k']

# create a new 'Append Attributes'
appendAttributes1 = AppendAttributes(registrationName='AppendAttributes1', Input=[paraview_chpvd, paraview_markerpvd])

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=appendAttributes1)
threshold1.Scalars = ['POINTS', 'k']
threshold1.ThresholdRange = [0.0, 648.0892796586917]

# Properties modified on threshold1
threshold1.Scalars = ['CELLS', 'k']
threshold1.ThresholdRange = [material_diffusivity, material_diffusivity]

# create a new 'Probe Location'
probeLocation1 = ProbeLocation(registrationName='ProbeLocation1', Input=threshold1,
    ProbeType='Fixed Radius Point Source')

# init the 'Fixed Radius Point Source' selected for 'ProbeType'
# probeLocation1.ProbeType.Center = [0.03, 0, 0.0044] # Original probe location
if dx == 5:
    probeLocation1.ProbeType.Center = [0.03375, 0, 0.0044] # Shifted probe location for voxel dx of 5mm
elif dx == 3:
    probeLocation1.ProbeType.Center = [0.03225, 0, 0.0044] # Shifted probe location for voxel dx of 3mm
elif dx == 2.5:
    probeLocation1.ProbeType.Center = [0.031875, 0, 0.0044] # Shifted probe location for voxel dx of 2.5mm
else:
    print("Voxel dx should be 5, 3 or 2.5")
    print("Setting the probe to the original location (30, 0, 4.4)")
    probeLocation1.ProbeType.Center = [0.03, 0, 0.0044] # Original probe location
    
# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=probeLocation1)

# save data
SaveData('probeTemp_imple2.csv', proxy=plotDataOverTime1, WriteTimeSteps=1,
    RowDataArrays=['N', 'Time', 'avg(X)', 'avg(Y)', 'avg(Z)', 'avg(k)', 'avg(rank)', 'avg(rank_input_1)', 'avg(vtkValidPointMask)', 'max(X)', 'max(Y)', 'max(Z)', 'max(k)', 'max(rank)', 'max(rank_input_1)', 'max(vtkValidPointMask)', 'med(X)', 'med(Y)', 'med(Z)', 'med(k)', 'med(rank)', 'med(rank_input_1)', 'med(vtkValidPointMask)', 'min(X)', 'min(Y)', 'min(Z)', 'min(k)', 'min(rank)', 'min(rank_input_1)', 'min(vtkValidPointMask)', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q1(k)', 'q1(rank)', 'q1(rank_input_1)', 'q1(vtkValidPointMask)', 'q3(X)', 'q3(Y)', 'q3(Z)', 'q3(k)', 'q3(rank)', 'q3(rank_input_1)', 'q3(vtkValidPointMask)', 'std(X)', 'std(Y)', 'std(Z)', 'std(k)', 'std(rank)', 'std(rank_input_1)', 'std(vtkValidPointMask)', 'vtkValidPointMask'],
    FieldAssociation='Row Data',
    AddTime=1)