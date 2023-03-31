#!/usr/bin/env python

import subprocess
import re
import math
import numpy as np
import matplotlib.pyplot as plt
import libconf
import pathlib as pl
import os
import glob
from PyPDF2 import PdfMerger
import shutil
import multiprocessing as mp
from clean_visualization import voxelPrinting
import sys

# measure process time
import time


def updateTemplateIndex(baseDirPathObj, versionDirTemplate, versionIndex):
    if versionIndex <= 0:
        versionIndex = 0
        while True:
            versionIndex += 1
            if not (baseDirPathObj / versionDirTemplate.format(versionIndex)).exists():
                break
    return versionIndex

def startRun(exePath, cfg, nProcs=1):
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
    
    with open('output.txt', 'w') as f:                              # run the program and save the output to output.txt
        f.write(' '.join(['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']))
        f.flush()
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings'], stdout=f) 
        # '-vec_view',':Vec1.m:ascii_matlab', '-mat_view',':filename.m:ascii_matlab'

def resumeRun(exePath, nProcs):
    with open('output.txt', 'a') as f:                              # run the program and save the output to output.txt
        # add exepat and nprocs to the output file
        f.write(' '.join(['mpirun', '-n', str(nProcs), exePath, '-resume_from_checkpoint', '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings','\n']))
        f.flush()
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '-resume_from_checkpoint', '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings'], stdout=f) 

def extractInfoFromOutputFile(outReadMode):
    
    match = re.search("error = ([\d.e-]+)", str(outReadMode))
    err = float(match.group(1))
    
    # get float value from string example: Solve (global_average_sec): 0.449638
    match = re.search("Solve \(global_average_sec\): ([\d.e-]+)", \
        str(outReadMode))
    time_solve = -1 if match.group(1) == None else float(match.group(1)) 
    
    # get float value from string example: Assemble (global_average_sec): 0.151703
    match = re.search("Assemble \(global_average_sec\): ([\d.e-]+)", \
        str(outReadMode))
    time_assemble = -1 if match.group(1) == None else float(match.group(1))
    
    # get float value from string example: KSPSolve (global_average_sec): 0.295132
    match = re.search("KSPSolve \(global_average_sec\): ([\d.e-]+)", \
        str(outReadMode))
    time_ksp = -1 if match.group(1) == None else float(match.group(1))
    
    # get float value from string example: Update (global_average_sec): 0.000759391
    match = re.search("Update \(global_average_sec\): ([\d.e-]+)", \
        str(outReadMode))
    time_update = -1 if match.group(1) == None else float(match.group(1))
    
    # Print the error and time values
    # print("error: {0:.8f}, time_solve: {1:.8f}, time_assemble: {2:.8f}, \
        # time_ksp: {3:.8f}, time_update: {4:.8f}".format(err, time_solve, \
            # time_assemble, time_ksp, time_update))
    
    # create a dictionary to store the error and time values
    ErrorTime_dict = {'error': err, 'time_solve': time_solve, 'time_assemble': \
        time_assemble, 'time_ksp': time_ksp, 'time_update': time_update}
    
    return ErrorTime_dict

def getVersionDirs(runDirPathObj):
    versionDirs = [d for d in runDirPathObj.iterdir() if d.is_dir()]    # get all the directories in the run directory
    versionDirs.sort(key=lambda d: int(d.name.split('_')[1]))           # sort the directories by version number
    return versionDirs


def getAllInfo(runDirPathObj):
    
    versionDirs = getVersionDirs(runDirPathObj)
    
    listOfDicts = []
    errors      = []
    time_solve  = []
    time_assemble = []
    time_ksp    = []
    time_update = []
    
    for versionDir in versionDirs:  # Go through each directory and read the error and time from the output.txt file
        with open(versionDir / 'output.txt', 'r') as f:
            out = f.read()
             
        infoDict = extractInfoFromOutputFile(out)
        errors.append(infoDict['error'])
        time_solve.append(infoDict['time_solve'])
        time_assemble.append(infoDict['time_assemble'])
        time_ksp.append(infoDict['time_ksp'])
        time_update.append(infoDict['time_update'])
    
    # create a dictionary to store the error and time values
    listOfDicts = {'error': errors, 'time_solve': time_solve, 'time_assemble': \
        time_assemble, 'time_ksp': time_ksp, 'time_update': time_update}
    return listOfDicts

def getError(runDirPathObj):
    errors = getAllInfo(runDirPathObj)['error']
    return errors

def getTime(runDirPathObj):
    listOfDicts = getAllInfo(runDirPathObj)
    Time_dict   = {'time_solve': listOfDicts['time_solve'], 'time_assemble': \
        listOfDicts['time_assemble'], 'time_ksp': listOfDicts['time_ksp'], \
            'time_update': listOfDicts['time_update']}
    print(Time_dict)
    return Time_dict
def createLatestDir(baseDirPathObj, dirTemplate):
    runDirIndex = updateTemplateIndex(baseDirPathObj, dirTemplate, 0)
    runDir = dirTemplate.format(runDirIndex)
    runDirPathObj = baseDirPathObj / runDir
    runDirPathObj.mkdir(parents=True, exist_ok=True)        # create the run directory
    return runDirPathObj    

def createConfig(paraDict):    
    cfgDict = {
        "elemOrder": 1,
        "AirDiffusivity": 0.1,
        "mesh": {
            "refine_lvl_base": 2,
            "refine_lvl_channel_wall": 2,
            "enable_subda": "false",
            "min": [0.0, 0.0, 0.0],
            "max": [1.0, 1.0, 1.0],
            "refine_walls": "true"
        },
        "solver_options_ht": {
            "ksp_max_it": 500,
            "ksp_type": "bcgs",
            "pc_type": "asm",
            "ksp_atol": 1e-15,
            "ksp_rtol": 1e-15,
            "ksp_converged_reason": ""
        },
        
        "dt": 0.01,
        "totalT": 7.0,
        "numTimestepPerVoxel": 3,
        "plateTemperature": 1.0,
        "voxelTemperature": 2.0,
        "voxelOrderFilename": paraDict['voxelOrderFilename'],
        "voxelInfo": {
            "voxelDiffusivity": paraDict['voxelDiffusivity'],
            "refine_level_voxel": paraDict['refine_level_voxel'],
        },
        "outputSpan": paraDict['outputSpan'],
        "checkpointFrequency": 1,
        "numberOfBackups": 2,
        "stepRunBreakPoints_V": paraDict['stepRunBreakPoints_V']
    }
    
    return cfgDict
    
def createAllConfigs(paraDict):
    cfgParaDict = { 'voxelOrderFilename': paraDict['voxelOrderFilename'], \
        'refine_level_voxel': paraDict['refine_level_voxel'],
        'stepRunBreakPoints_V': paraDict['stepRunBreakPoints_V'],
        'outputSpan': paraDict['outputSpan'],
        "voxelDiffusivity": paraDict['voxelDiffusivity']}
    
    cfg = createConfig(cfgParaDict)
    
    return cfg

def runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate, versionTemplate):
    
    cfg = createAllConfigs(paraDict)
    
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    
    print("cwd: ",os.getcwd())  # print the current working directory
    
    printGeom = paraDict['voxelOrderFilename']
    
    # Create a timetaken.txt file to store the time taken for each version
    timeTakenFile = open("timetaken.txt", "w")
    timeTakenFile.write("Geometry file: " + printGeom + "\n")
    startOverall = time.time()
    
    versionDirPathObj = createLatestDir(runDirPathObj, versionTemplate)
    
    # Create data directory inside the version directory
    dataDirPathObj = createLatestDir(versionDirPathObj, 'data')
    os.chdir(dataDirPathObj)
    
    shutil.copyfile(baseDirPathObj / printGeom, dataDirPathObj / printGeom)
    
    # measure time across the startRun
    startRun_time = time.time()
    startRun(exePath, cfg, 8)
    endRun_time = time.time()
    timeTakenFile.write("startRun took " + str(endRun_time - startRun_time) + " seconds. \n")
    timeTakenFile.flush()
    
    for j in paraDict["stepRunNumProcs"]:
        # measure time across the resumeRun
        startResume_time = time.time()
        resumeRun(exePath, j)
        endResume_time = time.time()
        # write time taken for resumeRun along with j value to the timetaken.txt file
        timeTakenFile.write("resumeRun with j = " + str(j) + " took " + str(endResume_time - startResume_time) + " seconds. \n")
        timeTakenFile.flush()
    
    # move "config.txt", printGeom, "output.txt", "repro.cfg" to the version directory
    shutil.move(dataDirPathObj / 'config.txt', versionDirPathObj / 'config.txt')
    shutil.move(dataDirPathObj / printGeom, versionDirPathObj / printGeom)
    shutil.move(dataDirPathObj / 'output.txt', versionDirPathObj / 'output.txt')
    # shutil.move(dataDirPathObj / 'repro.cfg', versionDirPathObj / 'repro.cfg')

    # if doFileCleanup:
    #     geomFilePath = versionDirPathObj / printGeom
    #     geom = voxelPrinting(geomFilePath, versionDirPathObj)
    
    os.chdir(runDirPathObj)
    
    endOverall = time.time()
    timeTakenOverall = endOverall - startOverall
    timeTakenFile.write("Overall time {0:.2f} seconds \n".format(timeTakenOverall))
    timeTakenFile.flush()
        
    timeTakenFile.close()
    return

def geometryParaCombination(geoName, numNodes):
    
    if geoName == "bunny_32_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 5,
            'stepRunNumProcs': [8],
            'stepRunBreakPoints_V': [1000000],
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008
        }
        
    if geoName == "bunny_64_sparse0.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'stepRunNumProcs': [16, 32, 72, 72],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000],
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4
        }
    
    if geoName == "bunny_64_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'stepRunNumProcs': [8],
            'stepRunBreakPoints_V': [100000],
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4
        }
    
    if geoName == "bunny_64_sparse2.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'stepRunNumProcs': [16, 32, 72, 72],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000],
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4
        }
        
    if geoName == "bunny_64_sparse4.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'stepRunNumProcs': [16, 32, 72, 72],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000],
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 8:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'stepRunNumProcs': [            16,    32,    96,    192,   288],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 6:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'stepRunNumProcs': [16, 32, 96, 216, 216, 216],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000, 200000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 4:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'stepRunNumProcs': [16, 32, 72, 96, 144, 144],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000, 200000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
    
    if geoName == "bunny_256_sparse2.csv" and numNodes == 4:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 8,
            'stepRunNumProcs': [            16,    32,    96,    144],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000 ],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
        
    if geoName == "bunny_256_sparse2.csv" and numNodes == 8:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 8,
            'stepRunNumProcs': [            16,    32,    96,    144,   288],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
        
    if geoName == "Moai_32.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 5,
            'stepRunNumProcs': [8],
            'stepRunBreakPoints_V': [20000],
            'outputSpan': 2,
            'voxelDiffusivity': 0.0008
        }
    
    if geoName == "Moai_64.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'stepRunNumProcs': [16, 32, 72, 72],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000],
            'outputSpan': 10,
            'voxelDiffusivity': 0.0008/4
        }
    
    if geoName == "Moai_128.csv" and numNodes == 8:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'stepRunNumProcs': [            16,    32,    96,    192,   288],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
        
    return paraDict
              
if __name__ == "__main__":
    
    versionTemplate = "config_{0:03d}"
    # versionTemplate = "procs_{0:03d}"
    isComputeSystem_local = False
    
    # Check the length of the command line arguments
    if len(sys.argv) != 3:
        geomName = "bunny_128_sparse2.csv"
        numNodes = 8
    else:
        geomName = sys.argv[1]
        numNodes = int(sys.argv[2])
    
    # ************ Local ************
    if isComputeSystem_local:
        baseDirPathObj  = pl.Path("/media/dhruv/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/runs/adm_runs/tests")
        exePath         = "/media/dhruv/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/cmake-build-3d-dendrite_kt/adm"
        runTemplate     = "local_run_{0:03d}"
        # numNodes = 1
        # numCPU = 1
    # *******************************
    
    # ************ NOVA ************
    if not isComputeSystem_local:
        baseDirPathObj  = pl.Path("/work/mech-ai/dgamdha/projects/leap_hi/software/runs/adm_runs/tests")
        exePath         = "/work/mech-ai/dgamdha/projects/leap_hi/software/admanufacturing/build/adm"
        runTemplate     = "nova_run_{0:03d}"
        # numNodes = 2
        # numCPU = 8
    # *******************************
    print("Number of processors:", mp.cpu_count())
    # paraDict = geometryParaCombination("bunny_64_sparse2.csv", 2)
    # paraDict = geometryParaCombination("bunny_128_sparse2.csv", 8)
    # paraDict = geometryParaCombination("bunny_128_sparse2.csv", 4)
    paraDict = geometryParaCombination(geomName, numNodes)
    
    runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate, versionTemplate)