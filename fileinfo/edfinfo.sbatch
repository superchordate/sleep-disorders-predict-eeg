#!/bin/bash

#SBATCH --job-name=edfinfo
#SBATCH --output=log/edfinfo.out
#SBATCH --error=log/edfinfo.err
#SBATCH --array=0-10
#SBATCH --time=03:00:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=1

# the environment variable SLURM_ARRAY_TASK_ID contains
# the index corresponding to the current job step
module load Anaconda3/5.3.0
python fileinfo/edfinfo.py $SLURM_ARRAY_TASK_ID