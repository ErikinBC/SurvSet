#!/bin/bash

# (i) Build conda environment if it does not exist
source set_env.sh

# (ii) Define R executables
R_path=$(which R)
Rs_path=$(which Rscript)

# (iii) Check that R versions lines up with conda environment expectation
version_conda=$(cat conda_env.txt | grep r-base | awk '{split($0,a,"r-base-"); print a[2]}' | awk '{split($0, a, "-"); print a[1]}')
version_Rs=$($R_path --version | grep "R version" | awk '{split($0,a,"version "); print a[2]}' | awk '{split($0,a," "); print a[1]}')

if [[ "$version_conda" != "$version_Rs" ]]; then
    echo "Versions are not aligned!! Exiting script"
    return
fi

# (iv) Install R packages
# $Rs_path install_libs.R

# (v) Loop through package-specific scripts
fn_process=$(ls process | grep .R$)
for fn in $fn_process; do
    echo "--- Processing package "$fn" ---"
    # $Rs_path process/$fn
done


