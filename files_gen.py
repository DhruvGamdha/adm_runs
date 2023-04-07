
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
        "numTimestepPerVoxel": 3,
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
        "stepRunBreakPoints_V": paraDict['stepRunBreakPoints_V']
    }
    
    return cfgDict


def geometryParaCombination(geoName, numNodes):
    
    if geoName == "bunny_32_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 5,
            'stepRunNumProcs': [8, 8, 8, 8],
            'stepRunBreakPoints_V': [1000, 2000, 4000, 8000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008,
            'checkpointFrequency': 10
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
    
    if geoName == "Moai_128.csv" and numNodes == 5:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'stepRunNumProcs': [            16,    32,    96,    192,   320],
            'stepRunBreakPoints_V': [10000, 20000, 40000, 80000, 160000],
            'outputSpan': 1000,
            'voxelDiffusivity': 0.0008/16
        }
        
    return paraDict


def NOVA_jobScript_writer(paraDict, isJobType_start, nProcs):
    
    exePath = paraDict['exePath']
    jobName = paraDict['jobName']
    
    # Evaluate the number of nodes needed
    if nProcs%64 == 0:
        numNodes = nProcs/64
    else:
        numNodes = nProcs/64 + 1 
    
    jobScriptHeader = """
    #!/bin/bash
    
    #SBATCH --time=24:00:00   # walltime limit (HH:MM:SS)
    #SBATCH --nodes={}   # number of nodes
    #SBATCH --ntasks-per-node=64   # 64 processor core(s) per node 
    #SBATCH --mem=369G   # maximum memory per node
    #SBATCH --job-name= {}   # job name
    #SBATCH --partition=amd    # amd node(s)
    #SBATCH --mail-user=dgamdha@iastate.edu   # email address
    #SBATCH --mail-type=BEGIN
    #SBATCH --mail-type=END
    #SBATCH --mail-type=FAIL
    
    """.format(numNodes, jobName)
     
    startJobScript = jobScriptHeader + \
    """
    
    mpirun -n {} {}
    
    """.format(nProcs, exePath)
    
    resumeJobScript = jobScriptHeader + \
    """
    
    mpirun -n {} {} -resume_from_checkpoint
    
    """.format(nProcs, exePath)
    
    if isJobType_start:
        return startJobScript
    else:
        return resumeJobScript

def local_jobScript_writer(paraDict, isJobType_start, nProcs):
    exePath = paraDict['exePath']
    
    startJobScript = """
    #!/bin/bash
    
    mpirun -n {} {}
    """.format(nProcs, exePath)
    
    resumeJobScript = """
    #!/bin/bash
     
    mpirun -n {} {} -resume_from_checkpoint
    """.format(nProcs, exePath)
    
    if isJobType_start:
        return startJobScript
    else:
        return resumeJobScript
    

def jobScripts_gen(paraDict, dataDirPathObj, computeSystem):
    
    jobScripts = []
    jobScriptsPath = []
    
    # Start job
    if computeSystem == "NOVA":
        jobScript = NOVA_jobScript_writer(paraDict, True, paraDict['stepRunNumProcs'][0])
    elif computeSystem == "local":
        jobScript = local_jobScript_writer(paraDict, True, paraDict['stepRunNumProcs'][0])
    jobScripts.append(jobScript)
    
    # Resume job
    for i in range(1, len(paraDict['stepRunNumProcs'])):
        if computeSystem == "NOVA":
            jobScript = NOVA_jobScript_writer(paraDict, False, paraDict['stepRunNumProcs'][i])
        elif computeSystem == "local":
            jobScript = local_jobScript_writer(paraDict, False, paraDict['stepRunNumProcs'][i])
        jobScripts.append(jobScript)
    
    # Write job scripts to files in the data directory
    for i in range(len(paraDict['stepRunNumProcs'])):
        jobScriptPath = dataDirPathObj + "/jobScript_{}.sh".format(i)
        with open(jobScriptPath, 'w') as f:
            f.write(jobScripts[i])
            f.close()
        print("Job script {} generated".format(jobScriptPath))
        jobScriptsPath.append(jobScriptPath)
    
    return jobScriptsPath