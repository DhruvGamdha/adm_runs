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
from configPara import geometryParaCombination, createConfig

# measure process time
import time
from utils import createLatestDir

def runExe(exePath, nProcs, isStartRun):
    with open('output.txt', 'w') as f:
        if isStartRun:
            command = ['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']
            f.write(' '.join(command))
            f.flush()
            subprocess.call(command, stdout=f)
        else:
            command = ['mpirun', '-n', str(nProcs), exePath, '-resume_from_checkpoint', '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']
            f.write(' '.join(command))
            f.flush()
            subprocess.call(command, stdout=f)
        f.close()
    return

def getVersionDirs(runDirPathObj):
    versionDirs = [d for d in runDirPathObj.iterdir() if d.is_dir()]    # get all the directories in the run directory
    versionDirs.sort(key=lambda d: int(d.name.split('_')[1]))           # sort the directories by version number
    return versionDirs

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

def runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate):
    
    cfg = createConfig(paraDict)
    
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    
    print("cwd: ",os.getcwd())  # print the current working directory
    
    printGeom = paraDict['voxelOrderFilename']
    
    # Create a timetaken.txt file to store the time taken for each version
    timeTakenFile = open("timetaken.txt", "w")
    timeTakenFile.write("Geometry file: " + printGeom + "\n")
    timeTakenFile.flush()
    startOverall = time.time()
    
    # Create data directory inside the version directory
    dataDirPathObj = createLatestDir(runDirPathObj, 'data')
    os.chdir(dataDirPathObj)
    
    shutil.copyfile(baseDirPathObj / printGeom, dataDirPathObj / printGeom)
    
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
        f.flush()
        f.close()
    
    runProcs = 1
    lastProcs = 0
    isStartRun = True
    counter = 0
    
    while True:  
        runProcs = getRunProcs(paraDict['baseProcs'], paraDict['maxProcs'], lastProcs)
        lastProcs = runProcs
        
        startRun_time = time.time()
        
        runExe(exePath, runProcs, isStartRun)
        
        endRun_time = time.time()
        
        if not isStartRun:
            # Check that the CheckPoint and CheckPoint_1 folders exist
            if not os.path.isdir('CheckPoint') or not os.path.isdir('CheckPoint_1'):
                raise ValueError("CheckPoint and CheckPoint_1 folders must exist.")
            
            # shutil.rmtree('CheckPoint') ## remove the CheckPoint folder
            # os.rename('CheckPoint_1', 'CheckPoint') ## Rename the CheckPoint_1 folder to CheckPoint
        
        isStartRun = False
            
        # Open the breakpoint.txt file and read the last line
        # Creata amountComplete variable to store a string
        amountComplete = ""
        with open('breakpoint.txt', 'r') as f:
            amountComplete = f.readlines()[-1]
            f.close()
        
        # write time taken for resumeRun along with j value to the timetaken.txt file
        timeTakenFile.write("Run "+ str(counter) +" with Procs = " + str(runProcs) + " took " + str(endRun_time - startRun_time) + " seconds, simulation progress = " + str(amountComplete) + " \n")
        timeTakenFile.flush()
        
        counter += 1
        
        # Check if "eos.txt" file exist in the directory, if so then break the loop
        if os.path.isfile("eos.txt"):
            break
    
    # move "config.txt", printGeom, "output.txt", "repro.cfg" to the version directory
    shutil.move(dataDirPathObj / 'config.txt', runDirPathObj / 'config.txt')
    shutil.move(dataDirPathObj / printGeom, runDirPathObj / printGeom)
    shutil.move(dataDirPathObj / 'output.txt', runDirPathObj / 'output.txt')
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

              
if __name__ == "__main__":
    
    versionTemplate = "config_{0:03d}"
    
    # Check the length of the command line arguments
    if len(sys.argv) != 4:
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
    
    # Check is baseDirPathObj and exePath exist
    if not os.path.isdir(baseDirPathObj) or not os.path.isfile(exePath):
        raise ValueError("baseDirPathObj and exePath must exist.")
        
    paraDict = geometryParaCombination(geomName, numNodes)
    
    runVoxelPrinting(exePath, paraDict, baseDirPathObj, runTemplate)