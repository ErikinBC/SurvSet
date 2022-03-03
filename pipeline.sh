#!/bin/bash

# Build conda environment if it does not exist
source set_env.sh

# (i) Download R package data
fold_pkgs='pkgs'
mirror='https://utstat.toronto.edu/cran'
echo "--- 1_download_pkgs.py ---"
python 1_download_pkgs.py --fold_pkgs $fold_pkgs --mirror $mirror

# (ii) Download website specific data
fold_custom='custom'
echo "--- 2_download_custom.py ---"
python 2_download_custom.py --fold_custom $fold_custom

# (iii) Loop through package-specific scripts
fold_output='output'
echo "--- 3_process.py ---"
python 3_process.py --fold_custom $fold_custom --fold_output $fold_output

# # (iv) Do QC checks on output files
fold_figures='figures'
min_num=4
python 4_check_QC.py --fold_output $fold_output --fold_figures $fold_figures --min_num $min_num

echo "~~~ End of pipeline.sh ~~~"