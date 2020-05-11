#!/bin/bash
#SBATCH --job-name=edf2csv
#SBATCH --output=log/edf2csv.out
#SBATCH --error=log/edf2csv.err
#SBATCH --time=01:00:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=52000

module load Anaconda3
python tocsv.py
