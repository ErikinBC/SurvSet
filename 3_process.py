# Script to call the different processing scripts
# Process MASS data
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_output', help='Name of the folder where output files will be written (default="output")', default='output')
args = parser.parse_args()
fold_output = args.fold_output
# fold_output='output'

import os
from funs_support import makeifnot
# Set directories
dir_base = os.getcwd()
dir_output = os.path.join(dir_base, fold_output)
makeifnot(dir_output)



# fn_process=$(ls process | grep .py$)
# n_process=$(ls process | wc -l)
# j=0
# for fn in $fn_process; do
#     j=$((j+1))
#     echo "--- Processing package "$fn" ("$j" of "$n_process") ---"
#     # python process/$fn
# done