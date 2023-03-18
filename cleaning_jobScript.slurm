#!/bin/bash

# Copy/paste this job script into a text file and submit with the command:
#    sbatch thefilename
# job standard output will go to the file slurm-%j.out (where %j is the job ID)

#SBATCH --time=10:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=36   # 64 processor core(s) per node 
#SBATCH --mem=369G   # maximum memory per node
#SBATCH --job-name="leap_hi_TSHT"
#SBATCH --mail-user=dgamdha@iastate.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
source $VENV/simple/bin/activate
cd /work/mech-ai/dgamdha/projects/leap_hi/software/runs/taly_run
python clean_visualization.py