
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
        
        "dt": paraDict['dt'],
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
        "voxelIncrementNumber": paraDict['voxelIncrementNumber'],
        "baseBreakPoint" : paraDict['baseBreakPoint'],
        "ifPrintStat": False,
        "ifPrintInfo": False
        
    }
    
    return cfgDict

def geometryParaCombination(geoName, numNodes):
    
    if geoName == "bunny_32_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 5,
            'baseProcs': 8,
            'maxProcs': 8,
            'baseBreakPoint' : 100000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.001,
            'checkpointFrequency': 10,
            'neumannBC':-0.1,
            'voxelIncrementNumber': 2,
            'dt': 0.01*2
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
            'neumannBC':-0.1/8,
            'voxelIncrementNumber': 16,
            'dt': 0.01*16
        }
    
    if geoName == "bunny_64_sparse2.csv" and numNodes == 1:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 6,
            'baseProcs': 8,
            'maxProcs': 128,
            'baseBreakPoint' : 10000,
            'outputSpan': 20,
            'voxelDiffusivity': 0.0008/4,
            'checkpointFrequency': 10,
            'neumannBC':-0.1/8,
            'voxelIncrementNumber': 16,
            'dt': 0.01*16
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
            'neumannBC':-0.1/8,
            'voxelIncrementNumber': 16,
            'dt': 0.01*16
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
            'neumannBC':-0.1/8,
            'voxelIncrementNumber': 16,
            'dt': 0.01*16
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
            'neumannBC':-0.1/64,
            'voxelIncrementNumber': 130,
            'dt': 0.01*130
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
            'neumannBC':-0.1/64,
            'voxelIncrementNumber': 130,
            'dt': 0.01*130
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
            'neumannBC':-0.1/64,
            'voxelIncrementNumber': 130,
            'dt': 0.01*130
        }
    
    if geoName == "bunny_128_sparse2.csv" and numNodes == 2:
        paraDict = {
            'voxelOrderFilename': geoName,
            'refine_level_voxel': 7,
            'baseProcs': 8,
            'maxProcs': 256,
            'baseBreakPoint' : 8000,
            'outputSpan': 100,
            'voxelDiffusivity': 0.0008/16,
            'checkpointFrequency': 100,
            'neumannBC':-0.1/64,
            'voxelIncrementNumber': 130,
            'dt': 0.01*130
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
            'neumannBC':-0.1/128,
            'voxelIncrementNumber': 1000,
            'dt': 0.01*1000
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
            'neumannBC':-0.1/128,
            'voxelIncrementNumber': 1000,
            'dt': 0.01*1000
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
            'neumannBC':-0.1,
            'voxelIncrementNumber': 2,
            'dt': 0.01*2
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
            'neumannBC':-0.1/8,
            'voxelIncrementNumber': 16,
            'dt': 0.01*16
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
            'neumannBC':-0.1/64,
            'voxelIncrementNumber': 130,
            'dt': 0.01*130
        }
        
    return paraDict