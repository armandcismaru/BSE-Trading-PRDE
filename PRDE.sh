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

python PRDE.py --experiment-type balancedGroups --k-value 5
python PRDE.py --experiment-type balancedGroups --k-value 7
python PRDE.py --experiment-type balancedGroups --k-value 8
python PRDE.py --experiment-type balancedGroups --k-value 10