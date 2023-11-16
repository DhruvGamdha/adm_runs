""" 
- This code is used to create 3D printing order of a voxelized wall (60 mm * 1.25 mm * 50 mm)
- The wall is created by stacking smaller walls (5 mm * 1.25 mm * 0.8 mm).
    - Since the width of both the walls are same, the larger wall is created by stacking of smaller wall by placing the smaller wall blocks along the x-axis (60 mm) and then moving to the next layer along the z-axis (50 mm).
    - The movement along the x-axis switches between forward and backward direction for each layer along the z-axis.
- The smaller wall is created by stacking voxels (0.05 mm * 0.05 mm * 0.05 mm) along the x-y plane (5 mm * 1.25 mm) and then moving to the next layer along the z-axis (0.8 mm).
    - The stacking of the voxels in the x-y plane is done by placing the voxels along the x-axis (5 mm) and then moving to the next layer along the y-axis (1.25 mm).
    - The movement along the x-axis switches between forward and backward direction for each layer along the y-axis.
    - Once the stacking of the voxels in the x-y plane is done, the next layer along the z-axis is created by moving along the z-axis (0.8 mm).
- The printing_order.csv file is created containing the indices of the voxels in the order in which they should be printed.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class VoxelizedWall:
    def __init__(self):
        # Dimensions of the larger wall
        wallWidth = 1.20  # y-axis
        # self.large_wall_dim = np.array([60, wallWidth, 50])  # x, y, z in mm
        self.large_wall_dim = np.array([8.0, wallWidth, 3.2])  # x, y, z in mm

        # User input for smaller wall dimensions
        self.small_wall_dim = np.array([
            float(input("Enter the length of the smaller wall along the x-axis in mm: ")),
            wallWidth,  # Width is the same
            float(input("Enter the height of the smaller wall along the z-axis in mm: "))
        ])

        # User input for voxel dimensions
        self.voxel_dim = np.array([
            float(input("Enter the voxel size along the x-axis in mm: ")),
            float(input("Enter the voxel size along the y-axis in mm: ")),
            float(input("Enter the voxel size along the z-axis in mm: "))
        ])

        # Calculate number of voxels in a small wall
        self.voxels_in_small_wall = np.ceil(self.small_wall_dim / self.voxel_dim).astype(int)
        
        # Print the number of voxels in a small wall
        print(f"\nNumber of voxels in a small wall: {self.voxels_in_small_wall[0]} * {self.voxels_in_small_wall[1]} * {self.voxels_in_small_wall[2]} = {np.product(self.voxels_in_small_wall)}")

        # Calculate number of small walls in the large wall
        self.small_walls_in_large_wall = np.ceil(self.large_wall_dim / self.small_wall_dim).astype(int)
        
        # Print the number of small walls in the large wall
        print(f"Number of small walls in the large wall: {self.small_walls_in_large_wall[0]} * {self.small_walls_in_large_wall[1]} * {self.small_walls_in_large_wall[2]} = {np.product(self.small_walls_in_large_wall)}")
        
        # Voxels (x,y,z) in the large wall
        self.voxels_in_large_wall = self.small_walls_in_large_wall * self.voxels_in_small_wall
        
        # Print the number of voxels in the large wall
        print(f"Number of voxels in the large wall: {self.voxels_in_large_wall[0]} * {self.voxels_in_large_wall[1]} * {self.voxels_in_large_wall[2]} = {np.product(self.voxels_in_large_wall)}")
        
        # Calculate the total number of operations for progress tracking
        num_small_walls = np.product(self.small_walls_in_large_wall)
        num_voxels_per_small_wall = np.product(self.voxels_in_small_wall)
        self.total_operations = 2*(num_small_walls * num_voxels_per_small_wall)
        self.current_operation = 0
        
        self.create_large_wall()
        
    def update_progress(self):
        self.current_operation += 1
        progress = (self.current_operation / self.total_operations) * 100
        print(f"\rProgress: {progress:.2f}%", end="")

    def create_small_wall(self):
        wall = np.zeros(self.voxels_in_small_wall, dtype=int)
        voxel_id = 1
        for z in range(wall.shape[2]):
            for y in range(wall.shape[1]):
                x_range = range(wall.shape[0]) if y % 2 == 0 else range(wall.shape[0] - 1, -1, -1)
                for x in x_range:
                    wall[x, y, z] = voxel_id
                    voxel_id += 1
                    self.update_progress()  # Update progress
        return wall

    def create_large_wall(self):
        self.large_wall = np.zeros(self.small_walls_in_large_wall, dtype=object)
        for z in range(self.large_wall.shape[2]):
            x_range = range(self.large_wall.shape[0]) if z % 2 == 0 else range(self.large_wall.shape[0] - 1, -1, -1)
            for x in x_range:
                for y in range(self.large_wall.shape[1]):
                    self.large_wall[x, y, z] = self.create_small_wall()
                    self.update_progress()  # Update progress

    def save_printing_order(self):
        printing_order = []
        for z in range(self.large_wall.shape[2]):
            for x in range(self.large_wall.shape[0]):
                for y in range(self.large_wall.shape[1]):
                    small_wall = self.large_wall[x, y, z]
                    for sw_z in range(small_wall.shape[2]):
                        for sw_y in range(small_wall.shape[1]):
                            sw_x_range = range(small_wall.shape[0]) if sw_y % 2 == 0 else range(small_wall.shape[0] - 1, -1, -1)
                            for sw_x in sw_x_range:
                                voxel_id = small_wall[sw_x, sw_y, sw_z]
                                if voxel_id > 0:
                                    # Calculate global voxel indices
                                    global_x = x * self.voxels_in_small_wall[0] + sw_x
                                    global_y = y * self.voxels_in_small_wall[1] + sw_y
                                    global_z = z * self.voxels_in_small_wall[2] + sw_z
                                    printing_order.append([global_x, global_y, global_z])
                                    self.update_progress()  # Update progress
                                
        print("\nSaving printing order...")
        order_df = pd.DataFrame(printing_order, columns=['X', 'Y', 'Z'])
        order_df.to_csv('printing_order.csv', index=False, sep=' ')
        

# Usage
wall = VoxelizedWall()
wall.save_printing_order()

print("\nPrinting order for the voxelized wall has been saved as a CSV file.")
