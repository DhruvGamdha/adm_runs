#!/usr/bin/env python

import pathlib as pl
import os
import sys
from configPara import geometryParaCombination, createConfig

# measure process time
from utils import createLatestDir, prepareDirectories, changeDirectory, setupRunEnvironment, runSimulation, cleanupAndArchiveData, paraviewStuff, runCoolDown


def runVoxelPrinting(exePath, 
                     paraDict, 
                     baseDirPathObj, 
                     runTemplate,
                     computeSystem):
    
    timeTakenFileName = "timetaken.txt"
    eosFileName = "eos.txt"
    
    cfg = createConfig(paraDict)
    
    testsDir_po, geoDir_po = prepareDirectories(baseDirPathObj)
    
    runDirPathObj = createLatestDir(testsDir_po, runTemplate)
    
    changeDirectory(runDirPathObj) 
    
    printGeom = paraDict['voxelOrderFilename']
    printGeomDense = paraDict['voxelOrderDenseFilename']
    
    dataDirPathObj = setupRunEnvironment(runDirPathObj, 
                                         geoDir_po, 
                                         printGeom, 
                                         printGeomDense, 
                                         cfg)
    
    runSimulation(exePath, 
                  paraDict, 
                  timeTakenFileName, 
                  dataDirPathObj, 
                  eosFileName,
                  computeSystem)
    
    runCoolDown(exePath, 
                timeTakenFileName, 
                dataDirPathObj,
                computeSystem)
    
    if dataDirPathObj/ eosFileName:
        print("Simulation completed successfully.")
        print("Cleaning up and archiving data.")
        cleanupAndArchiveData(runDirPathObj, timeTakenFileName, dataDirPathObj)
        paraviewStuff(baseDirPathObj, dataDirPathObj)
    
    return
              
if __name__ == "__main__":
    
    # versionTemplate = "config_{0:03d}"
    
    # Check the length of the command line arguments
    # assert len(sys.argv) == 5, "Usage: python convergencet.py <geomName> <denseGeomName> <numNodes> <computeSystem>"
    if len(sys.argv) == 4:
        geomName = sys.argv[1]
        denseGeomName  = ""
        numNodes = int(sys.argv[2])
        computeSystem = sys.argv[3]
    elif len(sys.argv) == 5:
        geomName = sys.argv[1]
        denseGeomName  = sys.argv[2]
        numNodes = int(sys.argv[3])
        computeSystem = sys.argv[4]
    else:
        geomName = "bunny_32_sparse2.csv"
        denseGeomName  = "bunny_32_zeroSparsity.csv"
        numNodes = 1
        computeSystem = 'local' # 'local', 'nova', 'anvil', 'frontera'
    
    # ************ Local ************
    if computeSystem == 'local':
        baseDirPathObj  = pl.Path("/media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/")
        exePath         = "/media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/build_release/adm"
        runTemplate     = "local_run_{0:03d}"
    # *******************************
    
    # ************ NOVA ************
    if computeSystem =='nova':
        baseDirPathObj  = pl.Path("/work/mech-ai/dgamdha/projects/leap_hi/software/runs/adm_runs/")
        exePath         = "/work/mech-ai/dgamdha/projects/leap_hi/software/admanufacturing/build/adm"
        runTemplate     = "nova_run_{0:03d}"
    # *******************************
    
    # ************ ANVIL ************
    if computeSystem =='anvil':
        baseDirPathObj  = pl.Path("/anvil/scratch/x-dgamdha/projects/leap_hi/software/runs/adm_runs/")
        exePath         = "/anvil/projects/x-cts110007/x-dgamdha/projects/leap_hi/software/admanufacturing/build_advance/adm"
        runTemplate     = "anvil_run_{0:03d}"
    # *******************************
    
    # ************ FRONTERA ************
    if computeSystem =='frontera':
        baseDirPathObj  = pl.Path("/scratch1/09374/dgamdha/projects/leaphi/adm_runs/")
        exePath         = "/work2/09374/dgamdha/frontera/projects/leaphi/softwares/admanufacturing/build_release/adm"
        runTemplate     = "frontera_run_{0:03d}"
    # *******************************
    
    # Check is baseDirPathObj and exePath exist
    if not os.path.isdir(baseDirPathObj) or not os.path.isfile(exePath):
        raise ValueError("baseDirPathObj and exePath must exist.")
        
    paraDict = geometryParaCombination(geomName, 
                                       denseGeomName,
                                       numNodes, 
                                       computeSystem)
    
    runVoxelPrinting(exePath, 
                     paraDict, 
                     baseDirPathObj, 
                     runTemplate,
                     computeSystem)