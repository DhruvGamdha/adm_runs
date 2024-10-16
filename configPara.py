
def createConfig(paraDict):
    
    # Check if paraDict['checkpointFrequency'] exists and if not create it with a default value of 1
    if 'checkpointFrequency' not in paraDict:
        paraDict['checkpointFrequency'] = 1 
        
    if 'refine_lvl_base' not in paraDict:
        paraDict['refine_lvl_base'] = 4
        
    cfgDict = {
        "elemOrder": 1,
        "AirDiffusivity": 0.0000197,
        "mesh": {
            "refine_lvl_base": paraDict['refine_lvl_base'],
            "refine_lvl_channel_wall": 2,
            "enable_subda": "false",
            "min": [0.0, 0.0, 0.0],
            "max": paraDict['mesh_max'],
            "physicalDomainMax": paraDict['mesh_physicalDomainMax'],
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
        "numTimestepPerVoxel": paraDict['numTimestepPerVoxel'],
        "thermConductivity": 0.2,
        "convectCoeff": -30,
        "ambientTemperature" : 368.15,
        "emissivity": 0,
        "curr_UPre_dampFactor": 1.0,
        
        "plateTemperature": 373.15,
        "voxelTemperature": 528.15,
        "voxelOrderFilename": paraDict['voxelOrderFilename'],
        "voxelInfo": {
            "voxelDiffusivity": 9.0e-8,
            "refine_level_voxel": paraDict['refine_level_voxel'],
        },
        "outputSpan": paraDict['outputSpan'],
        "checkpointFrequency": paraDict['checkpointFrequency'],
        "numberOfBackups": 2,
        "voxelIncrementNumber": paraDict['voxelIncrementNumber'],
        "baseBreakPoint" : paraDict['baseBreakPoint'],
        "ifPrintStat": False,
        "ifPrintInfo": True,
        "ifPrintWarn": False,
        "coolDownNumTimesteps": paraDict['coolDownNumTimesteps']
    }
    
    return cfgDict

def geometryParaCombination(geoName, numNodes, computeSystem):
    
    if computeSystem == 'anvil':
        if geoName == "Cube_voxRes_32.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 5,
                'baseProcs': 8,
                'maxProcs': 128,
                'baseBreakPoint' : 3000,
                'outputSpan': 200,
                'checkpointFrequency': 1000000,
                'voxelIncrementNumber': 2,
                'dt': 0.01*2,
                'numTimestepPerVoxel': 4
            }
        
        if geoName == "bunny_32_zeroSparsity.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 5,
                'baseProcs': 16,
                'maxProcs': 32,
                'baseBreakPoint' : 100000,
                'outputSpan': 100,
                'checkpointFrequency': 10,
                'voxelIncrementNumber': 2,
                'dt': 2.318*2/10,
                'numTimestepPerVoxel':10,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08]
            }
            
        if geoName == "bunny_64_zeroSparsity.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 8,
                'maxProcs': 128,
                'baseBreakPoint' : 15000,
                'outputSpan': 500,
                'checkpointFrequency': 1000,
                'voxelIncrementNumber': 16,
                'dt': 0.01*16,
                'numTimestepPerVoxel': 4,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08]
            }
            
        if geoName == "bunny_64_zeroSparsity.csv" and numNodes == 2:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 8,
                'maxProcs': 256,
                'baseBreakPoint' : 3000,
                'outputSpan': 6000,
                'checkpointFrequency': 12000,
                'voxelIncrementNumber': 1,
                'dt': 0.01*1,
                'numTimestepPerVoxel': 4,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08]
            }
        
        if geoName == "bunny_128_zeroSparsity.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 7,
                'baseProcs': 32,
                'maxProcs': 128,
                'baseBreakPoint' : 48000,
                'outputSpan': 25,
                'checkpointFrequency': 10,
                'voxelIncrementNumber': 130,
                'dt': 0.0362*130/10,
                'numTimestepPerVoxel':10,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08]
            }
        
        if geoName == "bunny_256_zeroSparsity.csv" and numNodes == 4:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 8,
                'refine_lvl_base': 5,
                'baseProcs': 128,
                'maxProcs': 512,
                'baseBreakPoint' : 500000,
                'outputSpan': 10,
                'checkpointFrequency': 10,
                'voxelIncrementNumber': 1100,
                'dt': 0.00453*1100/10,
                'numTimestepPerVoxel':10,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08]
                
            }
            
        if geoName == "Moai_128_zeroSparsity.csv" and numNodes == 3:
            assert False, "Please find and fill the mesh_max and mesh_physicalDomainMax for Moai"
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 7,
                'baseProcs': 8,
                'maxProcs': 384,
                'baseBreakPoint' : 4000,
                'outputSpan': 50,
                'checkpointFrequency': 1000000,
                'voxelIncrementNumber': 130,
                'dt': 0.01*130,
                'numTimestepPerVoxel': 4,
                'mesh_max': [0,0,0],
                'mesh_physicalDomainMax': [0,0,0]
            }
    
    elif computeSystem == 'frontera':
        
        if geoName == "bunny_64_zeroSparsity.csv" and numNodes == 2:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 8,
                'maxProcs': 112,
                'baseBreakPoint' : 15000,
                'outputSpan': 20,
                'checkpointFrequency': 1000,
                'voxelIncrementNumber': 16,
                'dt': 0.2897*16/8,
                'numTimestepPerVoxel': 8,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08],
                'coolDownNumTimesteps': 5000
            }
        
        if geoName == "bunny_128_zeroSparsity.csv" and numNodes == 2:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 7,
                'baseProcs': 32,
                'maxProcs': 112,
                'baseBreakPoint' : 48000,
                'outputSpan': 25,
                'checkpointFrequency': 100,
                'voxelIncrementNumber': 130,
                'dt': 0.018*130/10,
                'numTimestepPerVoxel':10,
                'mesh_max': [0.08, 0.08, 0.08],
                'mesh_physicalDomainMax': [0.08, 0.08, 0.08],
                'coolDownNumTimesteps': 10000
            }
        
        if geoName == "printCorrected_3DBenchy_64R.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 8,
                'maxProcs': 56,
                'baseBreakPoint' : 30000,
                'outputSpan': 3,
                'checkpointFrequency': 1000,
                'voxelIncrementNumber': 16,
                'dt': 0.12739*16/4 ,
                'numTimestepPerVoxel': 4,
                'mesh_max': [0.06083, 0.06083, 0.06083],
                'mesh_physicalDomainMax': [0.06083, 0.06083, 0.06083],
                'coolDownNumTimesteps': 5000
            }
        
        if geoName == "printCorrected_3DBenchy_64R.csv" and numNodes == 2:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 8,
                'maxProcs': 112,
                'baseBreakPoint' : 15000,
                'outputSpan': 20,
                'checkpointFrequency': 1000,
                'voxelIncrementNumber': 16,
                'dt': 0.12739*16/8,
                'numTimestepPerVoxel': 8,
                'mesh_max': [0.06083, 0.06083, 0.06083],
                'mesh_physicalDomainMax': [0.06083, 0.06083, 0.06083],
                'coolDownNumTimesteps': 5000
            }
        
        if geoName == "printCorrected_3DBenchy_128R.csv" and numNodes == 2:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 7,
                'baseProcs': 32,
                'maxProcs': 112,
                'baseBreakPoint' : 48000,
                'outputSpan': 20,
                'checkpointFrequency': 100,
                'voxelIncrementNumber': 130,
                # 'dt': 0.0159*130/10,
                'dt': 0.00795*130/10,
                'numTimestepPerVoxel': 10,
                'mesh_max': [0.06083, 0.06083, 0.06083],
                'mesh_physicalDomainMax': [0.06083, 0.06083, 0.06083],
                'coolDownNumTimesteps': 10000
            }
    
    elif computeSystem == 'local':
        if geoName == "printCorrected_3DBenchy_64R.csv" and numNodes == 1:
            paraDict = {
                'voxelOrderFilename': geoName,
                'refine_level_voxel': 6,
                'baseProcs': 2,
                'maxProcs': 8,
                'baseBreakPoint' : 15000,
                'outputSpan': 4,
                'checkpointFrequency': 100,
                'voxelIncrementNumber': 16,
                'dt': 0.03185*16,
                'numTimestepPerVoxel': 4,
                'mesh_max': [0.06083, 0.06083, 0.06083],
                'mesh_physicalDomainMax': [0.06083, 0.06083, 0.06083],
                'coolDownNumTimesteps': 5000
            }
        
    return paraDict