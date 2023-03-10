import pathlib as pl
import os
import numpy as np

class voxelPrinting:
    
    def __init__(self, geomFilePath, datFilePath):
        self.geomFilePath   = geomFilePath
        self.printing_order = []
        self.numVoxels_xyz  = np.array([0, 0, 0])
        self.numNodes_xyz   = np.array([0, 0, 0])
        self.numVoxels     = 0
        self.numNodes     = 0
        self.datFilePath = datFilePath
        
        self.readGeomFile()
        self.readDatFile()
        
    def ijk2ID(self, i, j, k, type='voxel'):
        """
        Convert i, j, k indices to voxel ID
        """
        if type == 'voxel':
            assert i >= 0 and i < self.numVoxels_xyz[0], "ERROR: i index out of bounds"
            assert j >= 0 and j < self.numVoxels_xyz[1], "ERROR: j index out of bounds"
            assert k >= 0 and k < self.numVoxels_xyz[2], "ERROR: k index out of bounds"
            return i + j * self.numVoxels_xyz[0] + k * self.numVoxels_xyz[0] * self.numVoxels_xyz[1]
        
        if type == 'node':
            assert i >= 0 and i < self.numNodes_xyz[0], "ERROR: i index out of bounds"
            assert j >= 0 and j < self.numNodes_xyz[1], "ERROR: j index out of bounds"
            assert k >= 0 and k < self.numNodes_xyz[2], "ERROR: k index out of bounds"
            return i + j * self.numNodes_xyz[0] + k * self.numNodes_xyz[0] * self.numNodes_xyz[1]
        
        return -1
        
    def readDatFile(self):
        
        
    def readGeomFile(self):
        """
        Read voxel printing geometry file and return list of voxels in printing order.
        """
        numLayers   = 0 # number of layers in the geometry file
        numContours = 0 # number of contours in the geometry file
        numInfills  = 0 # number of infills in the geometry file
        
        geomFile = open(self.geomFilePath, 'r')
        
        # Check if the file is empty
        if os.stat(self.geomFilePath).st_size == 0:
            print("ERROR: Empty geometry file")
            return
        
        # Read the first line of the file
        line = geomFile.readline()
        words = line.split()
        
        identifier = words[0]
        numLayers = int(words[1])
        assert numLayers > 0, "ERROR: Number of layers must be greater than 0"
        
        # set the number of voxels in the x, y, and z directions
        self.numVoxels_xyz[0] = int(numLayers)
        self.numVoxels_xyz[1] = int(numLayers)
        self.numVoxels_xyz[2] = int(numLayers)
        self.numVoxels = self.numVoxels_xyz[0] * self.numVoxels_xyz[1] * self.numVoxels_xyz[2]
        
        
        # set the number of nodes in the x, y, and z directions
        self.numNodes_xyz[0] = int(numLayers) + 1
        self.numNodes_xyz[1] = int(numLayers) + 1
        self.numNodes_xyz[2] = int(numLayers) + 1
        self.numNodes = self.numNodes_xyz[0] * self.numNodes_xyz[1] * self.numNodes_xyz[2]
        
        for lNum in range(self.numVoxels_xyz[2]):
            layerNum = 0
            numContours_layer = 0
            numInfills_layer = 0
            
            # Read the next line of the file
            line = geomFile.readline()
            words = line.split()
            
            identifier = words[0]
            assert identifier == 'l', "ERROR: Expected 'l' identifier"
            layerNum            = int(words[1])
            numContours_layer   = int(words[2])
            numInfills_layer    = int(words[3])
            
            assert layerNum == lNum, "ERROR: Layer number mismatch"
            
            numContours += numContours_layer
            numInfills += numInfills_layer
            
            for cNum in range(numContours_layer):
                contourNum = 0
                numPoints = 0
                
                line = geomFile.readline()
                words = line.split()
                identifier = words[0]
                assert identifier == 'c', "ERROR: Expected 'c' identifier"
                
                contourNum = int(words[1])
                numPoints = int(words[2])
                
                line = geomFile.readline()
                words = line.split()
                
                for pNum in range(numPoints):
                    x = 0
                    y = 0
                    z = 0
                    y = int(words[pNum])
                    x = int(words[pNum + 1])
                    z = layerNum
                    
                    assert x >= 0 and x < self.numVoxels_xyz[0], "ERROR: x index out of bounds"
                    assert y >= 0 and y < self.numVoxels_xyz[1], "ERROR: y index out of bounds"
                    
                    voxelID = self.ijk2ID(x, y, z, type='voxel')
                    
                    # Check if the voxel is already in the list
                    if voxelID not in self.printing_order:
                        self.printing_order.append(voxelID)
                    
            
            for iNum in range(numInfills_layer):
                infillNum = 0
                numPoints = 0
                
                line = geomFile.readline()
                words = line.split()
                
                identifier = words[0]
                assert identifier == 'i', "ERROR: Expected 'i' identifier"
                 
                infillNum = int(words[1])
                numPoints = int(words[2])
                
                line = geomFile.readline()
                words = line.split()
                
                for pNum in range(numPoints):
                    x = 0
                    y = 0
                    z = 0
                    y = int(words[pNum])
                    x = int(words[pNum + 1])
                    z = layerNum
                    
                    assert x >= 0 and x < self.numVoxels_xyz[0], "ERROR: x index out of bounds"
                    assert y >= 0 and y < self.numVoxels_xyz[1], "ERROR: y index out of bounds"
                    
                    voxelID = self.ijk2ID(x, y, z, type='voxel')
                    
                    # Check if the voxel is already in the list
                    if voxelID not in self.printing_order:
                        self.printing_order.append(voxelID)
                    
        geomFile.close()
        
        print("Printing geometry file read successfully")
        print("Number of layers in z: {}".format(self.numVoxels_xyz[2]))
        print("Number of contours: {}".format(numContours))
        print("Number of infills: {}".format(numInfills))
        print("Number of voxels: {}".format(self.numVoxels))
        print("Number of nodes: {}".format(self.numNodes))
        print("Number of unique filled voxels: {}".format(len(self.printing_order)))
        
        
if __name__=="__main__":
    runDirID = 1
    geomName = 'LowResCube.ctr'
    
    runDirTemplate = "run_{:03d}"
    cwd = pl.Path.cwd()
    runDirPath = cwd / 'tests' / runDirTemplate.format(runDirID)

    print("Cleaning up visualization files in {}".format(runDirPath))
    dataDirPath = runDirPath / 'data'
    cleanDataDirPath = runDirPath / 'clean_data'
    
    # make clean data directory
    if not cleanDataDirPath.exists():
        cleanDataDirPath.mkdir()
    
    