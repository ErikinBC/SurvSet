"""
Contains shared parameters and functions in the _datagen module.
"""

# Packages
import os


##########################
# --- (1) PARAMETERS --- #

dir_base = os.getcwd()
dir_SurvSet = os.path.join(dir_base, 'SurvSet')
assert os.path.exists(dir_SurvSet), 'SurvSet package not found in the current directory!'
# Define the directories where the data will be stored
dir_resources = os.path.join(dir_SurvSet, 'resources')
dir_pkgs = os.path.join(dir_resources, 'pkgs')
dir_custom = os.path.join(dir_resources, 'custom')
dir_pickles = os.path.join(dir_resources, 'pickles')
dir_figures = os.path.join(dir_resources, 'figures')
lst_dir_data = [dir_pkgs, dir_custom, dir_pickles, dir_figures]
for d in lst_dir_data:
    if not os.path.exists(d):
        os.makedirs(d)
        print('Created folder in SurvSet package: %s' % d)


#################################
# --- (2) DEFAULT ARGUMENTS --- #

di_argpase_defaults = {
    'fold_pkgs': {'val': 'pkgs', 'type': str, 'help': 'Folder to store downloaded R packages'},
    
    'mirror': {'val': 'https://utstat.toronto.edu/cran', 'type': str, 'help': 'CRAN mirror URL to download R packages from'},
    
    'fold_custom': {'val': 'custom', 'type': str, 'help': 'Folder to store custom datasets downloaded from websites'},
        
    'fold_output': {'val': 'output', 'type': str, 'help': 'Folder to store processed datasets'},
    
    'fold_figures': {'val': 'figures', 'type': str, 'help': 'Folder to store QC figures'},
    
    'min_num': {'val': 4, 'type': int, 'help': 'Minimum number of categories required the the categorical variables'},

    'allow_overwrite': {'val': True, 'type': bool, 'help': 'Allow overwriting existing files in the output folder'},
    
    # '': {'val': ..., 'type': ..., 'help': ''},
}


