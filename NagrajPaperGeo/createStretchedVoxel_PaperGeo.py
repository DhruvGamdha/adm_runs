import numpy as np
import pandas as pd

class VoxelizedWall:
    def __init__(self):
        self.voxel_x_size = float(input("Enter the voxel size along the x-axis in mm: "))
        self.voxel_y_size = float(input("Enter the voxel size along the y-axis in mm: "))
        self.voxel_z_size = float(input("Enter the voxel size along the z-axis in mm: "))
        self.x_length = 60
        self.y_width = 1.25
        self.z_height = 50
        self.create_wall()

    def create_wall(self):
        self.x_voxels = int(np.ceil(self.x_length / self.voxel_x_size))
        self.y_voxels = int(np.ceil(self.y_width / self.voxel_y_size))
        self.z_voxels = int(np.ceil(self.z_height / self.voxel_z_size))

        print(f"Number of voxels along x: {self.x_voxels}")
        print(f"Number of voxels along y: {self.y_voxels}")
        print(f"Number of voxels along z: {self.z_voxels}")

        self.wall = np.zeros((self.x_voxels, self.y_voxels, self.z_voxels))
        voxel_id = 1
        for z in range(self.z_voxels):
            for x in range(self.x_voxels) if z % 2 == 0 else range(self.x_voxels - 1, -1, -1):
                for y in range(self.y_voxels):
                    self.wall[x, y, z] = voxel_id
                    voxel_id += 1

    def save_printing_order(self):
        printing_order = []
        for z in range(self.z_voxels):
            for x in range(self.x_voxels) if z % 2 == 0 else range(self.x_voxels - 1, -1, -1):
                for y in range(self.y_voxels):
                    voxel_id = self.wall[x, y, z]
                    printing_order.append([x, y, z])

        order_df = pd.DataFrame(printing_order, columns=['X', 'Y', 'Z'])
        order_df.to_csv('printing_order.csv', index=False, sep=' ')

# Usage
wall = VoxelizedWall()
wall.save_printing_order()

print(f"Voxelized wall created with voxel sizes {wall.voxel_x_size}x{wall.voxel_y_size}x{wall.voxel_z_size} mm.")
print("Printing order and voxel indices have been saved as CSV files.")
