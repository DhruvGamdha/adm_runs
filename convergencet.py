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
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '-ksp_rtol', \
            '1E-13'], stdout=f) # '-vec_view',':Vec1.m:ascii_matlab', '-mat_view',':filename.m:ascii_matlab'

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

def createConfig(paraDict, type=1):
    if type == 1:
        cfgDict = {
                "ifBoxGrid": True,
                "nsd": paraDict['nsd'],
                "basisFunction": paraDict['basisFunction'],
                "ifDD": paraDict['ifDD'],
                "Lx": 1,
                "Ly": 1,
                "Lz": 1,
                "Nelemx": paraDict['n_elems'],
                "Nelemy": paraDict['n_elems'],
                "Nelemz": paraDict['n_elems'],
                "typeOfIC": 1,
                "dt": paraDict['dt'],
                "nOfTS": int(paraDict['t']/paraDict['dt']),
            }
    elif type == 2:
        cfgDict = {
                "ifBoxGrid": True,
                "nsd": paraDict['nsd'],
                "basisFunction": paraDict['basisFunction'],
                "ifDD": paraDict['ifDD'],
                "Lx": 1,
                "Ly": 1,
                "Lz": 1,
                "Nelemx": paraDict['n_elems'],
                "Nelemy": paraDict['n_elems'],
                "Nelemz": paraDict['n_elems'],
                "typeOfIC": 1,
                "dt": paraDict['dt'],
                "dt_print": paraDict['dt_print'], 
                "additional_time": paraDict['additional_time'],
                "Tp": 50,
                "Ta": 30,
                "Tn": 70,
                "print_geometry_file": paraDict['printGeom'],
                "diffusivity": paraDict['diffusivity'],
                "K_ambient": 0,
                "outputExtension": '.dat'
            }
    return cfgDict

def createAllConfigs(dt_list, t_list = [1], nElems_list = [256], nsd_list = [2],\
    basisFunction_list  = ['linear'], ifDD=True, type=1):
    
    ## create all combinations of the config files parameters as a list of dictionaries
    allcfgsParams = []
    for dt in dt_list:
        for t in t_list:
            for n_elems in nElems_list:
                for nsd in nsd_list:
                    for basisFunction in basisFunction_list:
                        paraDict = {'dt': dt, 't': t, 'n_elems': n_elems, \
                                    'nsd': nsd, 'basisFunction': basisFunction,\
                                'ifDD': ifDD, 'type': type}
                        allcfgsParams.append(paraDict)            
    
    cfgsList = []
    for cfgParams in allcfgsParams:
        cfg = createConfig(cfgParams , type=type)
        cfgsList.append(cfg)
    
    return cfgsList
    
def createAllConfigs2(dt_list, dt_print_list, printGeom_list):
    allcfgsParams = []
    
    for dt in dt_list:
        for dt_print in dt_print_list:
            for printGeom in printGeom_list:
                paraDict = {'dt': dt, 'dt_print': dt_print, 'nsd': 3, 'basisFunction':\
                            'linear', 'ifDD': False, 'n_elems': 16, "additional_time":\
                                20, 'diffusivity': 0.002, 'printGeom': printGeom}
                allcfgsParams.append(paraDict)
    
    
    cfgList = []
    for cfgParams in allcfgsParams:
        cfg = createConfig(cfgParams, type=2)
        cfgList.append(cfg)
    
    return cfgList


def runVoxelPrinting(exePath, dt_list, dt_print_list, baseDirPathObj, \
    runTemplate, versionTemplate, printGeomList, numNodes, numCPU, doFileCleanup = True):
    
    # printGeom = 'LowResCube.ctr'
    # printGeom = 'bunny_16.ctr'
    
    cfg_list = createAllConfigs2(dt_list, dt_print_list, printGeomList)
    
    # cfg = createConfig(0.1, 1, 16, 3, 'linear', False, 2)
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    # print the current directory
    print(os.getcwd())
    
    for i in range(len(cfg_list)):
        cfg = cfg_list[i]
        printGeom = printGeomList[i]
        versionDirPathObj = createLatestDir(runDirPathObj, versionTemplate)
        
        # Create data directory inside the version directory
        dataDirPathObj = createLatestDir(versionDirPathObj, 'data')
        os.chdir(dataDirPathObj)
        
        # copy LowResCube.ctr file from baseDirPathObj to the current directory
        shutil.copyfile(baseDirPathObj / printGeom, dataDirPathObj / printGeom)
        
        runExe(exePath, cfg, numNodes*numCPU)
        
        # move "config.txt", printGeom, "output.txt", "repro.cfg" to the version directory
        shutil.move(dataDirPathObj / 'config.txt', versionDirPathObj / 'config.txt')
        shutil.move(dataDirPathObj / printGeom, versionDirPathObj / printGeom)
        shutil.move(dataDirPathObj / 'output.txt', versionDirPathObj / 'output.txt')
        shutil.move(dataDirPathObj / 'repro.cfg', versionDirPathObj / 'repro.cfg')

        if doFileCleanup:
            geomFilePath = versionDirPathObj / printGeom
            geom = voxelPrinting(geomFilePath, versionDirPathObj)
        
        os.chdir(runDirPathObj)
    
    return

      
if __name__ == "__main__":
    
    dtp             = 0.035
    dt_print_list   = [dtp]
    dts             = [dtp/3]
    # numProcs        = [1, 2, 4, 8]
    versionTemplate = "config_{0:03d}"
    # versionTemplate = "procs_{0:03d}"
    isComputeSystem_local = True
    
    # ************ Local ************
    if isComputeSystem_local:
        baseDirPathObj  = pl.Path("/media/dhruv/data/Dhruv/ISU/PhD/Projects/FEM/TalyFEM/runs/TSHT/plotting/python/tests")
        exePath         = "/media/dhruv/data/Dhruv/ISU/PhD/Projects/FEM/TalyFEM/taly_fem/cmake-build-release/tutorials/transient_heat/ht"
        runTemplate     = "local_run_{0:03d}"
        numNodes = 1
        numCPU = 8
    # *******************************
    
    # ************ NOVA ************
    if not isComputeSystem_local:
        baseDirPathObj  = pl.Path("/work/mech-ai/dgamdha/projects/leap_hi/software/runs/taly_run/tests")
        exePath         = "/work/mech-ai/dgamdha/projects/leap_hi/software/taly_4_3dprinting/build/tutorials/transient_heat/ht"
        runTemplate     = "nova_run_{0:03d}"
        numNodes = 4
        numCPU = 36
    # *******************************
    print("Number of processors:", mp.cpu_count())
    # printGeomList = ['LowResCube.ctr', 'bunny_16.ctr', 'bunny_32_sparse2.ctr', 'bunny_64_sparse2.ctr']
    printGeomList = ['bunny_16.ctr', 'bunny_16.ctr']
    
    runVoxelPrinting(exePath, dts, dt_print_list, baseDirPathObj, runTemplate, \
        versionTemplate, printGeomList, numNodes, numCPU, True)