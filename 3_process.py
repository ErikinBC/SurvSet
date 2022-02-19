# Script to call the different processing scripts
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_output', help='Name of the folder where output files will be written (default="output")', default='output')
args = parser.parse_args()
fold_output = args.fold_output
# fold_output='output'

# (i) Set directories
import os
import pandas as pd
from pydoc import locate
from funs_support import makeifnot, str_subset

dir_base = os.getcwd()
dir_output = os.path.join(dir_base, fold_output)
dir_pkgs = os.path.join(dir_base, 'pkgs')
makeifnot(dir_output)

# (ii) Baseline columns for all datasets
cn_surv = ['pid', 'time', 'event']
cn_surv2 = ['pid', 'time', 'time2', 'event']

# (iii) Find all processing files and run
fn_process = pd.Series(os.listdir('process'))
fn_process = str_subset(fn_process, '\\.py$')
n_process = len(fn_process)

for j, fn_py in enumerate(fn_process):
    fn = fn_py.replace('.py','')
    print('--- Processing package %s (%i of %i) ---' % (fn, j+1, n_process))
    path_fn = 'process.%s' % fn
    processor = getattr(locate(path_fn), 'package')
    # Set attributes
    processor = processor(pkg=fn, dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
    # Get list of methods
    methods = str_subset(dir(processor),'^process\\_')
    for method in methods:
        getattr(processor, method)()

print('~~~ End of 3_process.py ~~~')
