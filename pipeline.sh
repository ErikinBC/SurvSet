#!/bin/bash

# Build conda environment if it does not exist
source set_env.sh

# (i) Download R package data
fold_pkgs='pkgs'
mirror='https://utstat.toronto.edu/cran'
python 1_download_pkgs.py --fold_pkgs $fold_pkgs --mirror $mirror

return

# (ii) Download website specific data
fold_custom='custom'
python 2_download_custom.py --fold_custom $fold_custom

# (iii) Loop through package-specific scripts
fold_output='output'
python 3_process.py --fold_output $fold_output



echo "~~~ End of pipeline.sh ~~~"