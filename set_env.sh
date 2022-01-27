#!/bin/bash

env_name=SurvSet
# Check to see if miniconda environment exists
grep_env=$(ls ~/miniconda3/envs | grep $env_name)
n_char=$(echo $grep_env | wc -w)

if [[ "$n_char" -eq 0 ]]; then
    echo "Installing environment"
    # (i) For replication
    # conda create --name $env_name --file conda_env.txt python=3.7
    # (ii) For initialization
    conda create --name $env_name python python=3.9
    conda activate $env_name
    conda install -c conda-forge r-base=4.0.3  # numpy pandas plotnine scikit-learn 
    # conda install gxx_linux-64
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
