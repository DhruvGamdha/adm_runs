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
from utils import createLatestDir

def startRun(exePath, cfg, nProcs=1):
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
    
    with open('output.txt', 'w') as f:                              # run the program and save the output to output.txt
        f.write(' '.join(['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']))
        f.flush()
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings'], stdout=f) 
        # '-vec_view',':Vec1.m:ascii_matlab', '-mat_view',':filename.m:ascii_matlab'

def resumeRun(exePath, nProcs):
    
    ## remove the CheckPoint folder
    shutil.rmtree('CheckPoint')
    
    ## Rename the CheckPoint_1 folder to CheckPoint
    os.rename('CheckPoint_1', 'CheckPoint')
    
    with open('output.txt', 'a') as f:                              # run the program and save the output to output.txt
        # add exepat and nprocs to the output file
        f.write(' '.join(['mpirun', '-n', str(nProcs), exePath, '-resume_from_checkpoint', '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings','\n']))
        f.flush()
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '-resume_from_checkpoint', '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings'], stdout=f) 

def getVersionDirs(runDirPathObj):
    versionDirs = [d for d in runDirPathObj.iterdir() if d.is_dir()]    # get all the directories in the run directory
    versionDirs.sort(key=lambda d: int(d.name.split('_')[1]))           # sort the directories by version number
    return versionDirs

def createConfig(paraDict):
    
    # Check if paraDict['checkpointFrequency'] exists and if not create it with a default value of 1
    if 'checkpointFrequency' not in paraDict:
        paraDict['checkpointFrequency'] = 1 
        
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
            "ksp_atol": 1e-6,
            "ksp_rtol": 1e-6,
            "ksp_converged_reason": ""
        },
        
        "dt": 0.01,
        "totalT": 7.0,
        "numTimestepPerVoxel": 4,
        "neumannBC":paraDict['neumannBC'],
        "plateTemperature": 1.0,
        "voxelTemperature": 2.0,
        "voxelOrderFilename": paraDict['voxelOrderFilename'],
        "voxelInfo": {
            "voxelDiffusivity": paraDict['voxelDiffusivity'],
            "refine_level_voxel": paraDict['refine_level_voxel'],
        },
        "outputSpan": paraDict['outputSpan'],
        "checkpointFrequency": paraDict['checkpointFrequency'],
        "numberOfBackups": 2,
        "baseBreakPoint" : paraDict['baseBreakPoint']
    }
    
    return cfgDict

def getRunProcs(baseProcs, maxProcs, lastProcs):
    if not all(x > 0 for x in [baseProcs, maxProcs]):
        raise ValueError("baseProcs, maxProcs arguments must be greater than zero.")
    
    if not (lastProcs >= 0):
        raise ValueError("lastProcs must be greater than or equal to zero.")
    
    # Check that maxProcs is greater than or equal to baseProcs and lastProcs
    if maxProcs < baseProcs or maxProcs < lastProcs:
        raise ValueError("maxProcs must be greater than or equal to baseProcs and lastProcs.")
    
    multiplier = 1
    newProcs = 0
    
    while True:
        newProcs = baseProcs*multiplier
        
        # Check that newProcs don't exceed maxProcs
        if newProcs >= maxProcs:
            newProcs = maxProcs
            break
        
        # Check if newProcs exceed lastProcs, 
        if newProcs > lastProcs:
            break
        multiplier = 2 * multiplier
    return newProcs

def runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate, versionTemplate):
    
    cfg = createConfig(paraDict)
    
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
    
    runProcs = 1
    lastProcs = 0
    isStartRun = True
    counter = 0
    
    while True:  
        runProcs = getRunProcs(paraDict['baseProcs'], paraDict['maxProcs'], lastProcs)
        lastProcs = runProcs
        
        startResume_time = time.time()
        
        if isStartRun:
            startRun(exePath, cfg, runProcs)
            isStartRun = False
        else:
            resumeRun(exePath, runProcs)

        endResume_time = time.time()
        
        # Open the breakpoint.txt file and read the last line
        # Creata amountComplete variable to store a string
        amountComplete = ""
        with open('breakpoint.txt', 'r') as f:
            amountComplete = f.readlines()[-1]
        
        # write time taken for resumeRun along with j value to the timetaken.txt file
        timeTakenFile.write("Run "+ str(counter) +" with Procs = " + str(runProcs) + " took " + str(endResume_time - startResume_time) + " seconds, simulation progress = " + str(amountComplete) + " \n")
        timeTakenFile.flush()
        
        counter += 1
        
        # Check if "eos.txt" file exist in the directory, if so then break the loop
        if os.path.isfile("eos.txt"):
            break
    
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
            'baseProcs': 8,
            'maxProcs': 8,
            'baseBreakPoint' : 1000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008,
            'checkpointFrequency': 10,
            'neumannBC':-0.1
        }
        
    if geoName == "bunny_64_sparse0.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 72,
            'baseBreakPoint' : 10000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8
        }
    
    if geoName == "bunny_64_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 72,
            'baseBreakPoint' : 10000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8
        }
    
    if geoName == "bunny_64_sparse2.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 72,
            'baseBreakPoint' : 10000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8
        }
        
    if geoName == "bunny_64_sparse4.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 72,
            'baseBreakPoint' : 10000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 8:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 288,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/64
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 6:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 216,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/64
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 4:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 144,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/64
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 256,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/64
        }
    
    if geoName == "bunny_256_sparse2.csv" and numNodes == 4:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 8,
            'baseProcs': 8,
            'maxProcs': 144,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/128
        }
        
    if geoName == "bunny_256_sparse2.csv" and numNodes == 8:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 8,
            'baseProcs': 8,
            'maxProcs': 288,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/128
        }
        
    if geoName == "Moai_32.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 5,
            'baseProcs': 8,
            'maxProcs': 8,
            'baseBreakPoint' : 10000,
            'outputSpan': 2,
            'voxelDiffusivity': 0.0008,
            'checkpointFrequency': 10,
            'neumannBC':-0.1
        }
    
    if geoName == "Moai_64.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 72,
            'baseBreakPoint' : 10000,
            'outputSpan': 10,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8
        }
    
    if geoName == "Moai_128.csv" and numNodes == 5:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 320,
            'baseBreakPoint' : 10000,
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/64
        }
        
    return paraDict
              
if __name__ == "__main__":
    
    versionTemplate = "config_{0:03d}"
    
    # Check the length of the command line arguments
    if len(sys.argv) != 3:
        geomName = "bunny_32_sparse2.csv"
        numNodes = 1
        computeSystem = 'local' # 'local', 'nova', 'anvil'
    else:
        geomName = sys.argv[1]
        numNodes = int(sys.argv[2])
        computeSystem = sys.argv[3] # 'local', 'nova', 'anvil'
    
    # ************ Local ************
    if computeSystem == 'local':
        baseDirPathObj  = pl.Path("/media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/runs/adm_runs/tests")
        exePath         = "/media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/cmake-build-release/adm"
        runTemplate     = "local_run_{0:03d}"
    # *******************************
    
    # ************ NOVA ************
    if computeSystem =='nova':
        baseDirPathObj  = pl.Path("/work/mech-ai/dgamdha/projects/leap_hi/software/runs/adm_runs/tests")
        exePath         = "/work/mech-ai/dgamdha/projects/leap_hi/software/admanufacturing/build/adm"
        runTemplate     = "nova_run_{0:03d}"
    # *******************************
    
    # ************ ANVIL ************
    if computeSystem =='anvil':
        baseDirPathObj  = pl.Path("/anvil/scratch/x-dgamdha/projects/leap_hi/software/runs/adm_runs/tests")
        exePath         = "/anvil/projects/x-cts110007/x-dgamdha/projects/leap_hi/software/admanufacturing/build/adm"
        runTemplate     = "anvil_run_{0:03d}"
    # *******************************
    print("Number of processors:", mp.cpu_count())
    paraDict = geometryParaCombination(geomName, numNodes)
    
    runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate, versionTemplate)