import pathlib as pl
import os
import shutil
import libconf
import subprocess
import time

def updateTemplateIndex(baseDirPathObj, versionDirTemplate, versionIndex):
    if versionIndex <= 0:
        versionIndex = 0
        while True:
            versionIndex += 1
            if not (baseDirPathObj / versionDirTemplate.format(versionIndex)).exists():
                break
    return versionIndex

def createLatestDir(baseDirPathObj, dirTemplate):
    runDirIndex = updateTemplateIndex(baseDirPathObj, dirTemplate, 0)
    runDir = dirTemplate.format(runDirIndex)
    runDirPathObj = baseDirPathObj / runDir
    runDirPathObj.mkdir(parents=True, exist_ok=True)        # create the run directory
    
    print("Created directory: " + str(runDirPathObj))
    return runDirPathObj

def checkDirFileExists(pathObj, isDir=True, isRaiseError=True):
    
    checkResult = True
    
    if isDir:
        if not os.path.isdir(pathObj):
            checkResult = False
    else:
        if not os.path.isfile(pathObj):
            checkResult = False
            
    if not checkResult and isRaiseError:
        raise ValueError("File/Directory " + str(pathObj) + " must exist.")
    else:
        return checkResult
    
    
def runExe(exePath, nProcs, isStartRun, computeSystem, isCoolDown=False):
    try:
        if computeSystem == 'frontera':
            command = ['ibrun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']
        else:
            command = ['mpirun', '-n', str(nProcs), exePath, '--bind-to core', '--map-by numa:PE=1/2', '--report-bindings']

        # Add resume flag for a non-start run
        if not isStartRun:
            command.insert(-3, '-resume_from_checkpoint')
            
        # Add cool_down flag for a cool down run
        if isCoolDown:
            command.insert(-3, '-cool_down')

        with open('output.log', 'a' if not isStartRun else 'w') as f:
            f.write(' '.join(command) + '\n')
            f.flush()

            # Use subprocess.run to capture the exit code
            completed_process = subprocess.run(command, stdout=f)

            if completed_process.returncode != 0:
                print(f"Error: The subprocess returned with exit code {completed_process.returncode}")
                exit(completed_process.returncode)

    except Exception as e:
        print(f"An exception occurred: {e}")

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


def prepareDirectories(baseDir_po):
    """
    Prepare required directories for the run.
    """
    testsDir_po = baseDir_po / 'tests'
    geoDir_po = baseDir_po / 'geometries'

    checkDirFileExists(geoDir_po, True, True)
    
    if not checkDirFileExists(testsDir_po, True, False):
        testsDir_po.mkdir(parents=True, exist_ok=True)
    
    return testsDir_po, geoDir_po

def changeDirectory(newDirPathObj):
    """
    Change the current working directory.
    """
    os.chdir(newDirPathObj)
    print("cwd: ", os.getcwd())

def setupRunEnvironment(runDirPathObj, geoDir_po, printGeom, printGeomDense, cfg):
    """
    Set up the environment for running the simulation.
    """

    # Create data directory inside the version directory
    dataDirPathObj = createLatestDir(runDirPathObj, 'data')
    changeDirectory(dataDirPathObj)

    shutil.copyfile(geoDir_po / printGeom, dataDirPathObj / printGeom)
    
    if printGeomDense is not "":
        shutil.copyfile(geoDir_po / printGeomDense, dataDirPathObj / printGeomDense)
    
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
        f.flush()
        f.close()

    return dataDirPathObj

def evaluateCompletion(dataDirPathObj):
    """
    Evaluate the completion of the simulation.
    """
    amountComplete = ""
    lastProcs = 0
    try:
        with open(dataDirPathObj / 'breakpoint.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                amountComplete = lines[-2].strip()
                lastProcs = int(lines[-1].strip())
    except IOError:
        print("Error reading from breakpoint.txt")

    return amountComplete, lastProcs

def runSimulation(exePath, 
                  paraDict, 
                  timeTakenFileName, 
                  dataDirPathObj, 
                  eosFileName,
                  computeSystem):
    runProcs = 1
    lastProcs = 0
    isStartRun = True
    counter = 0
    
    # Create a time taken file to record the time taken for each run
    timeTakenFile = open(timeTakenFileName, 'a' if os.path.isfile(timeTakenFileName) else 'w')
    timeTakenFile.write("Geometry file: " + paraDict['voxelOrderFilename'] + "\n")
    timeTakenFile.flush()
    timeTakenFile.close()
    
    while True:
        runProcs = getRunProcs(paraDict['baseProcs'], paraDict['maxProcs'], lastProcs)
        
        startRun_time = time.time()
        runExe(exePath, runProcs, isStartRun, computeSystem, False)
        endRun_time = time.time()
        
        if not isStartRun:
            # Check that the CheckPoint and CheckPoint_1 folders exist
            checkDirFileExists(dataDirPathObj / 'CheckPoint', True)
            checkDirFileExists(dataDirPathObj / 'CheckPoint_1', True)
            
        isStartRun = False
        
        amountComplete, lastProcs = evaluateCompletion(dataDirPathObj)
        
        timeTakenFile = open(timeTakenFileName, 'a' if os.path.isfile(timeTakenFileName) else 'w')
        timeTakenFile.write(f"Run {counter} with Procs = {runProcs} took {endRun_time - startRun_time} seconds, simulation progress = {amountComplete}\n")
        timeTakenFile.flush()
        timeTakenFile.close()
        
        counter += 1

        if os.path.isfile(eosFileName):
            break

def runCoolDown(exePath, timeTakenFileName, dataDirPathObj, computeSystem):
    # Find the last procs used and restart the simulation with those procs with
    # resume_from_checkpoint and cool_down flags
    lastProcs = 0
    amountComplete = ""
    try:
        amountComplete, lastProcs = evaluateCompletion(dataDirPathObj)
    except Exception as e:
        print(f"An exception occurred: {e}")
        
    # Check if CheckPoint and CheckPoint_1 directories exist
    checkDirFileExists(dataDirPathObj / 'CheckPoint', True)
    checkDirFileExists(dataDirPathObj / 'CheckPoint_1', True)
    
    runProcs = lastProcs
    isStartRun = False
    isCoolDown = True
    
    startRun_time = time.time()
    runExe(exePath, runProcs, isStartRun, computeSystem, isCoolDown)
    endRun_time = time.time()
    
    timeTakenFile = open(timeTakenFileName, 'a' if os.path.isfile(timeTakenFileName) else 'w')
    timeTakenFile.write(f"Cool down run took {endRun_time - startRun_time} seconds.\n")
    timeTakenFile.flush()
    timeTakenFile.close()

def cleanupAndArchiveData(runDirPathObj, timeTakenFileName, dataDirPathObj):
    
    # Move all the non-directory files from data directory to the run directory
    allFiles = [f for f in dataDirPathObj.iterdir() if f.is_file()]
    for file in allFiles:
        shutil.move(file, runDirPathObj / file.name)
        
    # copy the last solution directory to the run directory
    solDirfrmt = 'cellData'
    lastSolDirStepCount = max([int(d.name[solDirfrmt.__len__():]) for d in dataDirPathObj.iterdir() if d.is_dir() and d.name.startswith(solDirfrmt)])
    lastSolDirName = solDirfrmt + str(lastSolDirStepCount)
    checkDirFileExists(dataDirPathObj / lastSolDirName, True)
    shutil.copytree(dataDirPathObj / lastSolDirName, runDirPathObj / lastSolDirName)

    os.chdir(runDirPathObj)
    
    tarStartTime = time.time()
    tarCommand = ['tar', '-czf', dataDirPathObj.name + '.tar.gz', dataDirPathObj.name]
    subprocess.run(tarCommand)
    tarEndTime = time.time()
    
    timeTakenFile = open(timeTakenFileName, 'a' if os.path.isfile(timeTakenFileName) else 'w')
    timeTakenFile.write(f"Archiving took {tarEndTime - tarStartTime} seconds\n")
    timeTakenFile.flush()
    timeTakenFile.close()    

def paraviewStuff(baseDirPathObj, dataDirPathObj):
    
    print("Start to create .pvd files ")
    
    pvdPythonScript = "generate_pvd.py"
    shutil.copyfile(baseDirPathObj / "paraview" / pvdPythonScript, dataDirPathObj / pvdPythonScript)
    
    os.chdir(dataDirPathObj)
    pythonScriptCommand = ['python', pvdPythonScript ]
    subprocess.run(pythonScriptCommand)
    os.chdir(baseDirPathObj)
    
    print("DONE: Created .pvd files")
    
    # copy pvSaveAnimation.py to the data directory
    pvSaveAnimationScript = "pvSaveAnimation.py"
    shutil.copyfile(baseDirPathObj / "paraview" / pvSaveAnimationScript, dataDirPathObj / pvSaveAnimationScript)
    print("DONE: Copied pvSaveAnimation.py")
    