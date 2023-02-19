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
        subprocess.call(['mpirun', '-n', str(nProcs), exePath, '-ksp_rtol', '1E-13'], stdout=f)

def extractInfoFromOutputFile(outReadMode):
    
    match = re.search("error = ([\d.e-]+)", str(outReadMode))
    err = float(match.group(1))
    
    # get float value from string example: Solve (global_average_sec): 0.449638
    match = re.search("Solve \(global_average_sec\): ([\d.e-]+)", str(outReadMode))
    time_solve = -1 if match.group(1) == None else float(match.group(1)) 
    
    # get float value from string example: Assemble (global_average_sec): 0.151703
    match = re.search("Assemble \(global_average_sec\): ([\d.e-]+)", str(outReadMode))
    time_assemble = -1 if match.group(1) == None else float(match.group(1))
    
    # get float value from string example: KSPSolve (global_average_sec): 0.295132
    match = re.search("KSPSolve \(global_average_sec\): ([\d.e-]+)", str(outReadMode))
    time_ksp = -1 if match.group(1) == None else float(match.group(1))
    
    # get float value from string example: Update (global_average_sec): 0.000759391
    match = re.search("Update \(global_average_sec\): ([\d.e-]+)", str(outReadMode))
    time_update = -1 if match.group(1) == None else float(match.group(1))
    
    # Print the error and time values
    # print("error: {0:.8f}, time_solve: {1:.8f}, time_assemble: {2:.8f}, time_ksp: {3:.8f}, time_update: {4:.8f}".format(err, time_solve, time_assemble, time_ksp, time_update))
    
    # create a dictionary to store the error and time values
    ErrorTime_dict = {'error': err, 'time_solve': time_solve, 'time_assemble': time_assemble, 'time_ksp': time_ksp, 'time_update': time_update}
    
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
    listOfDicts = {'error': errors, 'time_solve': time_solve, 'time_assemble': time_assemble, 'time_ksp': time_ksp, 'time_update': time_update}
    return listOfDicts

def getError(runDirPathObj):
    errors = getAllInfo(runDirPathObj)['error']
    return errors

def getTime(runDirPathObj):
    listOfDicts = getAllInfo(runDirPathObj)
    Time_dict   = {'time_solve': listOfDicts['time_solve'], 'time_assemble': listOfDicts['time_assemble'], 'time_ksp': listOfDicts['time_ksp'], 'time_update': listOfDicts['time_update']}
    print(Time_dict)
    return Time_dict

def evaluateSlope_loglog(x, y, xScale, yScale):
    # x_log = [math.log10(x_i) for x_i in x]
    # y_log = [math.log10(y_i) for y_i in y]
    if xScale == 'log':
        x_update = np.log10(x)
    else:
        x_update = x
    if yScale == 'log':
        y_update = np.log10(y)
    else:
        y_update = y
    
    m, b = np.polyfit(x_update, y_update, 1)
    return m

def plot_vals(dts, errors, fileName, xLabel, yLabel, xScale='log', yScale='log', makeComparison=False, plotAppend=False):
    
    slope = evaluateSlope_loglog(dts, errors, xScale, yScale)
    plt.plot(dts, errors, marker='.' , label='slope: {0:.8f}'.format(slope))  # plot the convergence
    if makeComparison:
        # plot y = x, y = x^2, y = x^3
        plt.plot(dts, dts, label='y = x')
        plt.plot(dts, [dt**2 for dt in dts], label='y = x^2')
        plt.plot(dts, [dt**3 for dt in dts], label='y = x^3')
        
    # plt.show()          # show the plot
    plt.xscale(xScale)       # log log scale
    plt.yscale(yScale)

    plt.xlabel(xLabel)        # label the plot
    plt.ylabel(yLabel)
    
    plt.title(fileName)
    
    plt.legend(bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=4) # add the legend
    plt.savefig(fileName + '.pdf', dpi=300, format='pdf',bbox_inches='tight')        # save the plot
    plt.close()          # close the plot
      
def createLatestDir(baseDirPathObj, dirTemplate):
    runDirIndex = updateTemplateIndex(baseDirPathObj, dirTemplate, 0)
    runDir = dirTemplate.format(runDirIndex)
    runDirPathObj = baseDirPathObj / runDir
    runDirPathObj.mkdir(parents=True, exist_ok=True)        # create the run directory
    return runDirPathObj    

def createConfig(dt, t, n_elems, nsd, basis_function):
    cfgDict = {
            "ifBoxGrid": True,
            "nsd": nsd,
            "basisFunction": basis_function,
            "ifDD": True,
            "Lx": 1,
            "Ly": 1,
            "Lz": 1,
            "Nelemx": n_elems,
            "Nelemy": n_elems,
            "Nelemz": n_elems,
            "typeOfIC": 1,
            "dt": dt,
            "nOfTS": int(t/dt)
        }
    return cfgDict

def createAllConfigs(dt_list, t_list = [1], nElems_list = [256], nsd_list = [2], basisFunction_list  = ['linear']):
    
    ## create all combinations of the config files parameters as a list of dictionaries
    cfgsParams = []
    for dt in dt_list:
        for t in t_list:
            for n_elems in nElems_list:
                for nsd in nsd_list:
                    for basis_function in basisFunction_list:
                        paraDict = {'dt': dt, 't': t, 'n_elems': n_elems, 'nsd': nsd, 'basis_function': basis_function}
                        cfgsParams.append(paraDict)            
    
    cfgsList = []
    for cfgParams in cfgsParams:
        cfg = createConfig(cfgParams['dt'], cfgParams['t'], cfgParams['n_elems'], cfgParams['nsd'], cfgParams['basis_function'])
        cfgsList.append(cfg)
    
    return cfgsList
    
def runTemporalConvergenceExec(exePath, dt_list, baseDirPathObj, runTemplate, versionTemplate):
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    
    cfg_list = createAllConfigs(dt_list, t_list = [1], nElems_list = [256], nsd_list = [2], basisFunction_list  = ['linear'])
    
    for cfg in cfg_list:
        versionDirPathObj = createLatestDir(runDirPathObj, versionTemplate)
        os.chdir(versionDirPathObj) # change to the version directory
        runExe(exePath, cfg, 8)     # run the executable
        # errors.append(get_error(exePath, cfg))
        os.chdir(runDirPathObj)

    errors =  getError(runDirPathObj)
    
    print("Errors: " + ", ".join(["{0:.2E}".format(e) for e in errors]))
    xscale = 'log'
    yscale = 'log'
    plot_vals(dt_list,      errors,     'transient_time_convergence',       'dt', 'l2_error', xScale=xscale, yScale=yscale, makeComparison=True)                 # plot the convergence
    plot_vals(dt_list[:4],  errors[:4], 'transient_time_convergence_4dts',  'dt', 'l2_error', xScale=xscale, yScale=yscale, makeComparison=True)    # plot the convergence for the first 3 dt values
    

def evalStrongScaling(exePath, numProcs_list, baseDirPathObj, runTemplate, versionTemplate):
    
    cfg = createConfig(0.1, 10, 256, 2, 'linear')
    
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    os.chdir(runDirPathObj) # change to the run directory
    
    for numProcs in numProcs_list:
        versionDirPathObj = createLatestDir(runDirPathObj, versionTemplate)
        os.chdir(versionDirPathObj)
        runExe(exePath, cfg, numProcs)
        os.chdir(runDirPathObj)
    
    timeDict = getAllInfo(runDirPathObj)
    
    # Divide the time by the time at 1 processor
    timeDict['time_solve']      =  [ timeDict['time_solve'][0] / x for x in timeDict['time_solve']]
    timeDict['time_assemble']   =  [ timeDict['time_assemble'][0] / x  for x in timeDict['time_assemble']]
    timeDict['time_ksp']        =  [ timeDict['time_ksp'][0] / x  for x in timeDict['time_ksp']]
    timeDict['time_update']     =  [ timeDict['time_update'][0] / x  for x in timeDict['time_update']]
    
    plot_vals(numProcs_list, timeDict['time_solve'], 'time_solve', 'numProcs', 'time (s)', xScale='linear', yScale='log', makeComparison=False, plotAppend=True)
    plot_vals(numProcs_list, timeDict['time_assemble'], 'time_assemble', 'numProcs', 'time (s)', xScale='linear', yScale='log', makeComparison=False, plotAppend=True)
    plot_vals(numProcs_list, timeDict['time_ksp'], 'time_ksp', 'numProcs', 'time (s)', xScale='linear', yScale='log', makeComparison=False, plotAppend=True)
    plot_vals(numProcs_list, timeDict['time_update'], 'time_update', 'numProcs', 'time (s)', xScale='linear', yScale='log', makeComparison=False, plotAppend=True)
    
    # Read all the pdf files in the run directory and combine them into a single pdf file
    pdfs = glob.glob("*.pdf")
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("weakScaling.pdf")
    merger.close()
    
    
      
if __name__ == "__main__":
    
    dts             = [0.2, 0.1, 0.05, 0.025, 0.0125]
    # errors          = [7.43E-07, 1.98E-07, 6.01E-08, 2.73E-08, 1.74E-08]
    # dts             = [0.1, 0.05, 0.025]
    # errors          = [7.58E-07, 1.95E-07, 5.07E-08]
    numProcs        = [1, 2, 4, 8]
    runTemplate     = "run_{0:03d}"
    # versionTemplate = "config_{0:03d}"
    versionTemplate = "procs_{0:03d}"
    baseDirPathObj  = pl.Path("/media/dhruv/data/Dhruv/ISU/PhD/Projects/FEM/TalyFEM/runs/TSHT/plotting/python/tests")
    exePath         = "/media/dhruv/data/Dhruv/ISU/PhD/Projects/FEM/TalyFEM/taly_fem/cmake-build-release/tutorials/transient_heat/ht"
    # runDirPathObj   = baseDirPathObj / "run_007"
    
    # runTemporalConvergenceExec(exePath, dts, baseDirPathObj, runTemplate, versionTemplate)
    # plot_vals(dts, errors)
    # getTime(runDirPathObj)
    evalStrongScaling(exePath, numProcs, baseDirPathObj, runTemplate, versionTemplate)
    # evalWeakScaling(exePath, numProcs, baseDirPathObj, runTemplate, versionTemplate)

