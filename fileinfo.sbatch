#!/bin/bash
#SBATCH --job-name=edf2csv
#SBATCH --output=log/edf2csv.out
#SBATCH --error=log/edf2csv.err
#SBATCH --time=03:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=6
#SBATCH --mem-per-cpu=6000

module load Anaconda3
python fileinfo.py
