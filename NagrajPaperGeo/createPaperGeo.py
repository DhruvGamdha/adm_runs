""" 
- This code creates a voxelized vertical wall (60 mm, 1.25 mm, 50 mm) with a voxel size as input parameter.
    - The wall is 60 mm long along the x-axis, 1.25 mm wide along the y-axis and 50 mm high along the z-axis.
    - The lower left corner of the wall is at the origin of the coordinate system.
- The code then creates a 3D printing order of the wall voxels and saves it as a .csv file.
    - The printing happens layer by layer from the bottom to the top.
    - The printing direction switches between layers. x-min to x-max for odd layers and x-max to x-min for even layers.
    - For a given layer and given x, the printing order is from y-min to y-max.
- The code also creates a .csv file with the voxel indices.
"""

import numpy as np
import pandas as pd

def create_wall(voxel_size):
    # Dimensions of the wall in mm
    x_length = 60
    y_width = 1.25
    z_height = 50

    # Number of voxels along each dimension
    x_voxels = int(np.ceil(x_length / voxel_size))
    y_voxels = int(np.ceil(y_width / voxel_size))
    z_voxels = int(np.ceil(z_height / voxel_size))
    
    # Print the number of voxels along each dimension
    print(f"Number of voxels along x: {x_voxels}")
    print(f"Number of voxels along y: {y_voxels}")
    print(f"Number of voxels along z: {z_voxels}")

    # Create the voxel grid for the wall
    wall = np.zeros((x_voxels, y_voxels, z_voxels))

    # Populate the wall grid with indices (1-based indexing for voxel ID)
    voxel_id = 1
    for z in range(z_voxels):
        for x in range(x_voxels) if z % 2 == 0 else range(x_voxels - 1, -1, -1):
            for y in range(y_voxels):
                wall[x, y, z] = voxel_id
                voxel_id += 1

    return wall, x_voxels, y_voxels, z_voxels

def save_printing_order(wall, x_voxels, y_voxels, z_voxels):
    # Create a list to hold the printing order data
    printing_order = []

    # Generate the printing order
    for z in range(z_voxels):
        for x in range(x_voxels) if z % 2 == 0 else range(x_voxels - 1, -1, -1):
            for y in range(y_voxels):
                voxel_id = wall[x, y, z]
                # printing_order.append([int(voxel_id), x, y, z])
                printing_order.append([x, y, z])

    # Convert to a DataFrame and save as space separated CSV file
    # order_df = pd.DataFrame(printing_order, columns=['VoxelID', 'X', 'Y', 'Z'])
    order_df = pd.DataFrame(printing_order, columns=['X', 'Y', 'Z'])
    order_df.to_csv('printing_order.csv', index=False, sep=' ')

voxel_size = float(input("Enter the voxel size in mm: "))
wall, x_voxels, y_voxels, z_voxels = create_wall(voxel_size)
save_printing_order(wall, x_voxels, y_voxels, z_voxels)
# save_voxel_indices(wall)

print(f"Voxelized wall created with voxel size {voxel_size}mm.")
print(f"Printing order and voxel indices have been saved as CSV files.")


