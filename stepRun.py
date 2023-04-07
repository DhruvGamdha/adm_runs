import subprocess
import libconf
import pathlib as pl
import os
import shutil
import sys

from files_gen import geometryParaCombination, createConfig, jobScripts_gen
from utils import createLatestDir

def submit_and_track_job_nova(jobScriptPath):
    
    # Submit the job and get the job id
    jobID = subprocess.check_output("sbatch {}".format(jobScriptPath), shell=True)
    jobID = jobID.decode('utf-8')
    jobID = jobID.split(' ')[-1]
    jobID = int(jobID)
    print("Job submitted with job ID: {}".format(jobID))
    
    # Track the job (sacct command) ID every 15 mins, sleep for 15 mins
    ''' 
    Command output example:
          State
     ----------
        TIMEOUT 
      CANCELLED 
      COMPLETED 
      COMPLETED 
      COMPLETED 
      COMPLETED 
      COMPLETED 
      COMPLETED  
    '''
    command = "sacct -j {} -o jobid,jobname,state --noheader | grep '{}[^\.]' | awk '{print $3}'".format(jobID, jobID)
    while True:
        jobStatus = subprocess.check_output( command, shell=True)
        
         
        
    
    

def runSimulation(exePath, paraDict, baseDirPathObj, runTemplate, geomDirPathObj, computeSystem):
    ''' 
    Steps:
    1. Create the directories
    2. Create the config file and copy the geometry file
    3. Create all the job scripts (slurm or local)
    4. Run the simulation (slurm or local)
        Create a file timetaken.txt to store the time taken for each job
        
        slurm:
        a. Submit the first job, get the job id
        b. Track the job (sacct command) ID every 15 mins, sleep for 15 mins
        c. When the job is not running, check if "eos.txt" exists
        d. If "eos.txt" exists, get the time value from the file and add it to the timetaken.txt 
        file, move the config, geometry, job script, output, and timetaken.txt files to a directory
        above.
        e. If "eos.txt" does not exist, remove the "CheckPoint" directory and rename the 
        "CheckPoint_1" directory to "CheckPoint" and check if "breakpoint.txt" exists         
            1. If "breakpoint.txt" exists, update the job script to the next one, read the value of 
            "breakpoint.txt" and get the time value and add it to the timetaken.txt file, then 
            remove the "breakpoint.txt" file
            2. If "breakpoint.txt" does not exist, do not change the jobscript then job timed 
            out, so add the job time to the timetaken.txt file
        f. Submit the job
        
        local:
        a. Start running the job
        b. Check if "eos.txt" exists
        c. If "eos.txt" exists, get the time value from the file and add it to the timetaken.txt 
        file, move the config, geometry, job script, output, and timetaken.txt files to a directory
        above.
        d. If "eos.txt" does not exist, remove the "CheckPoint" directory and rename the 
        "CheckPoint_1" directory to "CheckPoint" and check if "breakpoint.txt" exists         
            1. If "breakpoint.txt" exists, update the job script to the next one, read the value of 
            "breakpoint.txt" and get the time value and add it to the timetaken.txt file, then 
            remove the "breakpoint.txt" file
        f. Submit the job
    '''
    # Create the directories and change to data directory
    runDirPathObj = createLatestDir(baseDirPathObj, runTemplate)
    dataDirPathObj = createLatestDir(runDirPathObj, 'data')
    os.chdir(dataDirPathObj)
    
    # Create the config file and copy the geometry file
    cfg = createConfig(paraDict)
    with open('config.txt', 'w') as f:
        libconf.dump(cfg, f)
    
    shutil.copyfile(geomDirPathObj / paraDict['voxelOrderFilename'], dataDirPathObj / paraDict['voxelOrderFilename'])
    
    # Create all the job scripts (slurm or local)
    jobScripts_gen(paraDict, dataDirPathObj, computeSystem)
    
    # Run the simulation (slurm or local)

if __name__ == "__main__":
    
    versionTemplate = "config_{0:03d}"
    # versionTemplate = "procs_{0:03d}"
    isComputeSystem_local = True
    
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
        exePath         = "/media/dhruv/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/cmake-build-release/adm"
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
    
    runSimulation(exePath, paraDict, baseDirPathObj, runTemplate, versionTemplate)