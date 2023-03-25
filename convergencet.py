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

def runExe(exePath, cfg, nProcs=1):
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
    
    with open('output.txt', 'w') as f:                              # run the program and save the output to output.txt
        subprocess.call(['mpirun', '-n', str(nProcs), exePath], stdout=f) 
        # '-vec_view',':Vec1.m:ascii_matlab', '-mat_view',':filename.m:ascii_matlab'

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
            "voxelDiffusivity": 0.5,
            "refine_level_voxel": paraDict['refine_level_voxel'],
        },
        "outputSpan": 1,
        "checkpointFrequency": 100,
        "numberOfBackups": 2
    }
    
    return cfgDict
    
def createAllConfigs(voxelFilename_list, voxelRes_list):
    allcfgsParams = []
    
    # Check length of lists are equal
    if len(voxelFilename_list) != len(voxelRes_list):
        raise Exception("Length of lists are not equal")
    
    for i in range(len(voxelFilename_list)):
        voxelOrderFilename = voxelFilename_list[i]
        refine_level_voxel = voxelRes_list[i]
        paraDict = { 'voxelOrderFilename': voxelOrderFilename, \
            'refine_level_voxel': refine_level_voxel}
        allcfgsParams.append(paraDict)
    
    
    cfgList = []
    for cfgParams in allcfgsParams:
        cfg = createConfig(cfgParams)
        cfgList.append(cfg)
    
    return cfgList


def runVoxelPrinting(exePath, voxelFilename_list, voxelRes_list, baseDirPathObj, \
    runTemplate, versionTemplate, numNodes, numCPU):
    
    cfg_list = createAllConfigs(voxelFilename_list, voxelRes_list)
    
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    
    print("cwd: ",os.getcwd())  # print the current working directory
    
    # Create a timetaken.txt file to store the time taken for each version
    timeTakenFile = open("timetaken.txt", "w")
    
    for i in range(len(cfg_list)):
        
        start = time.time()
        
        cfg = cfg_list[i]
        printGeom = voxelFilename_list[i]
        versionDirPathObj = createLatestDir(runDirPathObj, versionTemplate)
        
        # Create data directory inside the version directory
        dataDirPathObj = createLatestDir(versionDirPathObj, 'data')
        os.chdir(dataDirPathObj)
        
        shutil.copyfile(baseDirPathObj / printGeom, dataDirPathObj / printGeom)
        
        runExe(exePath, cfg, numNodes*numCPU)
        
        # move "config.txt", printGeom, "output.txt", "repro.cfg" to the version directory
        shutil.move(dataDirPathObj / 'config.txt', versionDirPathObj / 'config.txt')
        shutil.move(dataDirPathObj / printGeom, versionDirPathObj / printGeom)
        shutil.move(dataDirPathObj / 'output.txt', versionDirPathObj / 'output.txt')
        shutil.move(dataDirPathObj / 'repro.cfg', versionDirPathObj / 'repro.cfg')

        # if doFileCleanup:
        #     geomFilePath = versionDirPathObj / printGeom
        #     geom = voxelPrinting(geomFilePath, versionDirPathObj)
        
        os.chdir(runDirPathObj)
        
        end = time.time()
        timeTaken = end - start
        timeTakenFile.write("Version {0:03d} took {1:0.2f} seconds to run \n".format(i, timeTaken))
        timeTakenFile.flush()
        
    timeTakenFile.close()
    return

      
if __name__ == "__main__":
    
    versionTemplate = "config_{0:03d}"
    # versionTemplate = "procs_{0:03d}"
    isComputeSystem_local = False
    
    # ************ Local ************
    if isComputeSystem_local:
        baseDirPathObj  = pl.Path("/media/dhruv/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/runs/adm_runs/tests")
        exePath         = "/media/dhruv/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/cmake-build-3d-dendrite_kt/adm"
        runTemplate     = "local_run_{0:03d}"
        numNodes = 1
        numCPU = 1
    # *******************************
    
    # ************ NOVA ************
    if not isComputeSystem_local:
        baseDirPathObj  = pl.Path("/work/mech-ai/dgamdha/projects/leap_hi/software/runs/adm_runs/tests")
        exePath         = "/work/mech-ai/dgamdha/projects/leap_hi/software/admanufacturing/build/adm"
        runTemplate     = "nova_run_{0:03d}"
        numNodes = 1
        numCPU = 8
    # *******************************
    print("Number of processors:", mp.cpu_count())
    # voxelFilename_list = ['bunny_32_sparse2.csv', 'bunny_64_sparse2.csv', 'bunny_128_sparse2.csv', 'bunny_256_sparse2.csv']
    # voxelRes_list = [5, 6, 7, 8]
    voxelFilename_list = ['bunny_64_sparse2.csv', 'bunny_128_sparse2.csv']
    voxelRes_list = [6, 7]
    # numProcs      = [8, 16, 64, 72]
    
    runVoxelPrinting(exePath, voxelFilename_list, voxelRes_list, baseDirPathObj, \
            runTemplate, versionTemplate, numNodes, numCPU)