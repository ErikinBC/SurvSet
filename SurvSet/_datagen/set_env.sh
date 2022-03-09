#!/bin/bash

# Check to see if anaconda/miniconda environment exists
env_name=SurvSet
path_conda=$(which conda)
path_conda=$(echo $path_conda | awk '{split($0,a,"3/"); print a[1]}')3
grep_env=$(ls $path_conda/envs | grep $env_name)
n_char=$(echo $grep_env | wc -w)

if [[ "$n_char" -eq 0 ]]; then
    echo "Installing environment"
    conda env create -f $env_name.yml
else
    echo "Environment already exists"
fi

conda activate $env_name

echo "~~~ End of set_env.sh ~~~"