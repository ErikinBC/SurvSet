#!/bin/bash

# Check to see if anaconda/miniconda environment exists
env_name=SurvSet
path_conda=$(which conda)
path_conda=$(echo $path_conda | awk '{split($0,a,"3/"); print a[1]}')3
grep_env=$(ls $path_conda/envs | grep $env_name)
n_char=$(echo $grep_env | wc -w)

status=1  # Set install option
if [[ "$n_char" -eq 0 ]]; then
    echo "Installing environment"
    if [[ "$status" -eq 0 ]]; then
        echo "Cloning conda environment from conda_env.txt"
        conda create --name $env_name --file conda_env.txt python=3.9
    else
        echo "Building conda from scratch"
        conda create --name $env_name python python=3.9
        conda activate $env_name
        conda install -c conda-forge numpy pandas plotnine scikit-learn rdata
    fi
else
    echo "Environment already exists"
    conda list --explicit > conda_env.txt
fi

conda activate $env_name

# # Check to see if pip-specific packages are installed
# pckgs_pip="patchworklib==0.3.1"
# for pckg in $pckgs_pip; do
#     echo "package: "$pckg
#     grep_env=$(conda env export | grep $pckg)
#     n_char=$(echo $grep_env | wc -w)
#     if [[ "$n_char" -eq 0 ]]; then
#         echo "Installing $pckg"
#         python3 -m pip install $pckg
#     else
#         echo "$pckg already exists"
#     fi
# done
