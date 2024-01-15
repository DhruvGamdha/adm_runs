import os
import tarfile
import shutil

def create_tar_gz(directory):
    """
    Create a .tar.gz archive for each subdirectory in the given directory.

    :param directory: Path to the directory containing subdirectories
    """
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)

        # Check if it is a directory
        if os.path.isdir(subdir_path):
            # Name of the tar.gz file
            tar_gz_name = f"{subdir_path}.tar.gz"

            # Create a tar.gz file
            with tarfile.open(tar_gz_name, "w:gz") as tar:
                tar.add(subdir_path, arcname=subdir)
            print(f"Created archive: {tar_gz_name}")
            
            # Delete the original directory
            shutil.rmtree(subdir_path)
            print(f"Deleted original directory: {subdir_path}")

# Example usage
directory_to_scan = "/media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/runs/adm_runs/tests/testing/bdf2/local_run_01/data"  # Replace with your directory path
create_tar_gz(directory_to_scan)
