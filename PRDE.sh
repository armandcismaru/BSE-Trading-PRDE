#!/usr/bin/env bash

#SBATCH --job-name coursework_fz19792
#SBATCH --partition teach_gpu
#SBATCH --time 2:30:00
#SBATCH --mem 32GB
#SBATCH --nodes 1
#SBATCH --gres gpu:1

# get rid of any modules already loaded
module purge
# load in the module dependencies for this script
module load "languages/anaconda3/2021-3.8.8-cuda-11.1-pytorch"

python PRDE.py --experiment-type bgr --k-value 6 --F-value 0.2 --n-days 7

python3 PRDE.py --experiment-type bgr --k-value 4 --n-days 7