# Script to download datasets not found in R packages

args = commandArgs(trailingOnly=T)
fold_custom = args[1]
fold_custom='custom'

# (i) Load utility functions
source('funs_support.R')

# () Folder to write into
dir_base = getwd()
dir_custom = file.path(dir_base, fold_custom)
makeifnot(dir_custom)


# --- (1) Employee Attrition --- #
url = 'https://raw.githubusercontent.com/IBM/employee-attrition-aif360/master/data/emp_attrition.csv'
path_write = file.path(dir_custom, get_fn_url(url))
download.file(url, path_write)

# --- (2) Lung Cancer --- #
# https://www.openml.org/d/1245
url = 'https://www.openml.org/data/get_csv/552598/phpl04K8a'
path_write = file.path(dir_custom, get_fn_url(url))
download.file(url, path_write)


# Note sure where the Chandan Reddy datasets are coming from: https://dmkd.cs.vt.edu/TUTORIAL/Survival/index.htm

