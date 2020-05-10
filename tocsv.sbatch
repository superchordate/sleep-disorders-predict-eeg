#!/bin/bash
#SBATCH --job-name=edf2csv
#SBATCH --output=log/edf2csv.out
#SBATCH --error=log/edf2csv.err
#SBATCH --time=03:00:00
#SBATCH --partition=broadwl
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=2000

module load Anaconda3
python tocsv.py
