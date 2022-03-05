# Script to call the different processing scripts
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_custom', help='Name of the folder where the custom datasets will be downloaded to (default="pkgs"', default='custom')
parser.add_argument('--fold_output', help='Name of the folder where output files will be written (default="output")', default='output')
args = parser.parse_args()
fold_output = args.fold_output
fold_custom = args.fold_custom
# fold_output='output';fold_custom='custom'

# (i) Set directories
import os
import pandas as pd
from pydoc import locate
from funs_support import makeifnot, str_subset, find_dir_base

dir_base = find_dir_base()
dir_pkgs = os.path.join(dir_base, 'pkgs')
dir_custom = os.path.join(dir_base, fold_custom)
dir_output = os.path.join(dir_base, fold_output)
makeifnot(dir_output)

# (ii) Baseline columns for all datasets
cn_surv = ['pid', 'event', 'time']
cn_surv2 = ['pid', 'event', 'time', 'time2']

# (iii) Find all R processing files and run
dir_Rprocess = os.path.join(dir_base, 'Rprocess')
fn_Rprocess = pd.Series(os.listdir(dir_Rprocess))
fn_Rprocess = str_subset(fn_Rprocess, '\\.py$')
n_process = len(fn_Rprocess)

for j, fn_py in enumerate(fn_Rprocess):
    fn = fn_py.replace('.py','')
    print('--- Processing R package %s (%i of %i) ---' % (fn, j+1, n_process))
    path_fn = 'Rprocess.%s' % fn
    processor = getattr(locate(path_fn), 'package')
    # Set attributes
    processor = processor(pkg=fn, dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
    processor.run_all()

# (iv) Find all custom processing scripts
dir_Cprocess = os.path.join(dir_base, 'Cprocess')
fn_Cprocess = pd.Series(os.listdir(dir_Cprocess))
fn_Cprocess = str_subset(fn_Cprocess, '\\.py$')
n_process = len(fn_Cprocess)

for j, fn_py in enumerate(fn_Cprocess):
    fn = fn_py.replace('.py','')
    print('--- Processing R package %s (%i of %i) ---' % (fn, j+1, n_process))
    path_fn = 'Cprocess.%s' % fn
    processor = getattr(locate(path_fn), 'package')
    # Set attributes
    processor = processor(dir_custom=dir_custom, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
    processor.run_all()

print('~~~ End of 3_process.py ~~~')
