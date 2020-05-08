#!/bin/bash
#SBATCH --job-name=edf2csv
#SBATCH --output=edf2csv.out
#SBATCH --error=edf2csv.err
#SBATCH --time=03:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem-per-cpu=2000

module load Anaconda3
python tocsv.py
