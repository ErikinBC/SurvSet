#!/bin/bash

# (i) Build conda environment if it does not exist
source set_env.sh

# (ii) Download R package data
fold_pkgs='pkgs'
mirror='https://utstat.toronto.edu/cran'
python 1_download_pkgs.py --fold_pkgs $fold_pkgs --mirror $mirror

# # (iii) Download website specific data
# fold_custom='custom'
# # python 2_download_custom.R --fold_custom $fold_custom

# # (iv) Loop through package-specific scripts
# fn_process=$(ls process | grep .py$)
# n_process=$(ls process | wc -l)
# j=0
# for fn in $fn_process; do
#     j=$((j+1))
#     echo "--- Processing package "$fn" ("$j" of "$n_process") ---"
#     # python process/$fn
# done


echo "~~~ End of pipeline.sh ~~~"