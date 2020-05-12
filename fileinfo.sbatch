#!/bin/bash
#SBATCH --job-name=fileinfo
#SBATCH --output=log/fileinfo.out
#SBATCH --error=log/fileinfo.err
#SBATCH --time=03:00:00
#SBATCH --partition=broadwl
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=58000

module load Anaconda3
python fileinfo.py
