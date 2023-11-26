import pathlib as pl
import os
import numpy as np

class voxelPrinting:
    
    def __init__(self, geomFilePath, verDirPath):
        self.printing_order = []
        self.numVoxels_xyz  = np.array([0, 0, 0])
        self.numNodes_xyz   = np.array([0, 0, 0])
        self.numVoxels      = 0
        self.numNodes       = 0
        self.geomFilePath   = geomFilePath
        # self.dataDirName    = 'data'
        # self.cleanPrefix    = 'clean'
        # self.dataFileType   = '.dat'
        # self.verDirPath     = verDirPath
        # self.dataFileID     = datFileID
        
        # self.dataDirPath      = self.verDirPath / self.dataDirName
        # self.cleanDataDirPath = self.verDirPath / str(self.cleanPrefix + '_' + self.dataDirName)
        
        # make clean data directory
        # if not self.cleanDataDirPath.exists():
        #     self.cleanDataDirPath.mkdir()
        
        self.readGeomFile()
        self.saveCSVFile()
        # self.createCleanFile()
        
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
    
    def ID2ijk(self, ID, type='voxel'):
        
        ''' 
        Convert voxel ID to i, j, k indices
        '''
        
        if type == 'voxel':
            assert ID >= 0 and ID < self.numVoxels, "ERROR: voxel ID out of bounds"
            k = ID // (self.numVoxels_xyz[0] * self.numVoxels_xyz[1])
            j = (ID - k * self.numVoxels_xyz[0] * self.numVoxels_xyz[1]) // self.numVoxels_xyz[0]
            i = ID - j * self.numVoxels_xyz[0] - k * self.numVoxels_xyz[0] * self.numVoxels_xyz[1]
            return i, j, k
        
        if type == 'node':
            assert ID >= 0 and ID < self.numNodes, "ERROR: node ID out of bounds"
            k = ID // (self.numNodes_xyz[0] * self.numNodes_xyz[1])
            j = (ID - k * self.numNodes_xyz[0] * self.numNodes_xyz[1]) // self.numNodes_xyz[0]
            i = ID - j * self.numNodes_xyz[0] - k * self.numNodes_xyz[0] * self.numNodes_xyz[1]
            return i, j, k
        
        return -1, -1, -1
    
    def saveCSVFile(self):
        ''' 
        Get indices of the voxels in printing order and save them in a csv file (i,j,k)
        '''
        
        # Create the csv file
        csvFileName = self.geomFilePath.stem + '.csv'
        print('csv file name    :',csvFileName)
        
        # Get geoFile directory path
        geoDir = self.geomFilePath.parent
        
        csvFilePath = geoDir / csvFileName
        csvFile = open(csvFilePath, 'w')
        
        # Write the size of the printing_order to the csv file
        csvFile.write(str(len(self.printing_order)) + '\n')
        
        # Write the number of voxels in x, y, z directions to the csv file
        # csvFile.write(str(self.numVoxels_xyz[0]) + ' ' + str(self.numVoxels_xyz[1]) + ' ' + str(self.numVoxels_xyz[2]) + '\n')
        
        for ID in self.printing_order:
            i, j, k = self.ID2ijk(ID)
            # write i, j, k to csv file line by line: example: 0,0,0
            csvFile.write(str(i) + ' ' + str(j) + ' ' + str(k) + '\n')
             
        csvFile.close()
        
    def createCleanFile(self):
        '''
        Read the .dat file which contains the grid nodal values and the grid connectivity.
        
        Steps:
        1. Create the cleaned file inside the cleaned directory
        2. Open the cleaned file
        3. Open the original file
        4. Get the original file ID. Note that the original file ID indicated the number of voxels 
        printed from the printing order. This is the number of voxels that we will need to read 
        from the original file.
        5. Get the total number of nodes in the original file
        6. Transfer the file header to the cleaned file (i.e. the first 3 lines)
        7. Transfer the grid nodal values to the cleaned file
        8. Travel through the printing order till we reach the original file ID and transfer the
        the corresponding grid connectivity to the cleaned file.
        9. Close the files
        '''
        
        # self.datFileName      = self.dataDirName + '_' + str(self.dataFileID) + self.dataFileType
        # self.cleanFileName    = self.cleanPrefix + '_' + self.datFileName
        
        # Get list of all .dat files in the data directory
        datFileList = list(self.dataDirPath.glob('*.dat'))
        
        for datFilePath in datFileList:
            
            datFileName = datFilePath.name
            
            # Check if datFileName is data_init.dat or data_final.dat
            if datFileName == 'data_init.dat' or datFileName == 'data_final.dat':
                continue
        
            fileID = int(datFileName.split('_')[1].split('.')[0])
            cleanFileName = self.cleanPrefix + '_' + datFileName
            
            # Create the cleaned file inside the cleaned directory
            cleanFilePath = self.cleanDataDirPath / cleanFileName    
            cleanFile = open(cleanFilePath, 'w')
        
            # Open the original file
            origFile = open(datFilePath, 'r')
        
            # Get the total number of nodes in the original file
            numNodes = self.numNodes
            
            numVox2copy = 0
            # Check if the fileID is smaller than the number of voxels in printing order
            if fileID < len(self.printing_order):
                numVox2copy = fileID
            else:
                numVox2copy = len(self.printing_order)
            
            origLines = origFile.readlines()
            
            # Transfer the file header to the cleaned file (i.e. the first 3 lines)
            headerCount = 3
            for i in range(headerCount):
                if i<headerCount-1:
                    line = origLines[i]
                    cleanFile.write(line)
                else:
                    ''' 
                    example i=3 line : ZONE N=4913, E=4096, F=FEPOINT, ET=BRICK
                    Change the E=4096 to E=number of voxels to copy
                    '''
                    line = origLines[i]
                    words = line.split()
                    words[2] = 'E=' + str(numVox2copy) + ','
                    line = ' '.join(words)
                    # add a new line character
                    line = line + '\n'
                    cleanFile.write(line)
                
            # Transfer the grid nodal values to the cleaned file
            for i in range(numNodes):
                line = origLines[i + headerCount]
                cleanFile.write(line)
            
            referenceLineNum = headerCount + numNodes
            
            # Travel through the printing order till we reach the original file ID and transfer the
            # the corresponding grid connectivity to the cleaned file.
            for i in range(numVox2copy):
                voxID = self.printing_order[i]
                # print('voxID    :',voxID)
                line = origLines[referenceLineNum + voxID]
                cleanFile.write(line)
                
            # Close the files
            cleanFile.close()
            origFile.close()
        
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
            
            # If the line is empty, break the loop
            if not line:
                break
            
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
                
                self.fillPrintingOrder(words, numPoints, layerNum)
                  
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
                
                self.fillPrintingOrder(words, numPoints, layerNum)
                    
        geomFile.close()
        
        print("Printing geometry file read successfully")
        print("Number of layers in z: {}".format(self.numVoxels_xyz[2]))
        print("Number of contours: {}".format(numContours))
        print("Number of infills: {}".format(numInfills))
        print("Number of voxels: {}".format(self.numVoxels))
        print("Number of nodes: {}".format(self.numNodes))
        print("Number of unique filled voxels: {}".format(len(self.printing_order)))
        
    def fillPrintingOrder(self, words, numPoints, layerNum):
        for pNum in range(0, numPoints):
            x = 0
            y = 0
            z = 0
            y = int(words[2*pNum])
            x = int(words[2*pNum + 1])
            z = layerNum
            
            assert x >= 0 and x < self.numVoxels_xyz[0], "ERROR: x index out of bounds"
            assert y >= 0 and y < self.numVoxels_xyz[1], "ERROR: y index out of bounds"
            
            voxelID = self.ijk2ID(x, y, z, type='voxel')
            
            # Check if the voxel is already in the list
            if voxelID not in self.printing_order:
                self.printing_order.append(voxelID)
        
        
if __name__=="__main__":
    # set up parameters
    # runDirID = 6
    # verDirID = 1
    geomName = 'singleFilamentWall_256.ctr'
    # geomName = 'bunny_64.ctr'
    # set up file paths
    # runDirTemplate  = "local_run_{:03d}"
    # versDirTemplate = "config_{:03d}"
    
    cwd = pl.Path.cwd()
    # runDirPath       = cwd / 'tests' / runDirTemplate.format(runDirID)
    # verDirPath       = runDirPath / versDirTemplate.format(verDirID)
    # dataDirPath      = verDirPath / 'data'
    # cleanDataDirPath = verDirPath / 'clean_data'
    
    geoDirPath = cwd / 'geometries'
    geomFilePath = geoDirPath / geomName
    verDirPath = 'temp'
    geom = voxelPrinting(geomFilePath, verDirPath)