import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_pkgs', help='Name of the folder where the R packages will be downloaded to (default="pkgs"', default='pkgs')
parser.add_argument('--mirror', help='Mirror address for the CRAN packages', default='https://cloud.r-project.org/')
args = parser.parse_args()
fold_pkgs = args.fold_pkgs
mirror = args.mirror
# fold_pkgs='pkgs';mirror='https://utstat.toronto.edu/cran'

# Load other modules
import os
import pandas as pd
from urllib.request import urlretrieve
from funs_pkgs import di_pkgs
from funs_support import makeifnot, unzip, untar, find_dir_base

# Set up folders
dir_base = find_dir_base()
dir_pkgs = os.path.join(dir_base, fold_pkgs)
makeifnot(dir_pkgs)


###################################
# ---- (1) DOWNLOAD PACKAGES ---- #

# https://vincentarelbundock.github.io/Rdatasets/datasets.html

# (i) Find which have not been downloaded
all_pkgs = pd.Series(list(di_pkgs))
existing_pkgs = pd.Series(os.listdir(dir_pkgs))
# Some packages may have the period removed
p1 = all_pkgs.str.replace('\\.','',regex=True)
p2 = existing_pkgs.str.replace('\\.','',regex=True)
n_existing = len(existing_pkgs)
needed_pkgs = list(all_pkgs.loc[p1[~p1.isin(p2)].index])
n_pkgs = len(needed_pkgs)
print('%i packages need to be installed (%i fold in folder)' % (n_pkgs,n_existing))

# (ii) Download, extract, remove, and unzip
for j, pkg in enumerate(needed_pkgs):
    url_pkg = di_pkgs[pkg]
    fn_pkg = pd.Series(url_pkg).str.split('/')[0][-1]
    dest_pkg = os.path.join(dir_pkgs, fn_pkg)
    print('Downloading package = %s (%i of %i)' % (pkg, j+1, n_pkgs))
    urlretrieve(url=url_pkg,filename=dest_pkg)
    # Extract only the data folder
    fold_data = os.path.join(dir_pkgs, pkg, 'data')
    if not os.path.exists(fold_data):
        path_extract = os.path.join(pkg, 'data')
        # Extract the files from a specific folder
        untar(path_tar=dest_pkg,path_write=dir_pkgs,path_extract=path_extract)
        # See if files need to be unzipped
        dir_fn = os.path.join(dir_pkgs, path_extract)
        for fn in os.listdir(dir_fn):
            path = os.path.join(dir_fn, fn)
            unzip(path)
        assert os.path.exists(fold_data), 'untar did not unzip in the expected place!!'
        # Remove the tar file
        os.remove(dest_pkg)
        # Remove period from package name if it exists
        fold_src = os.path.join(dir_pkgs, pkg)
        fold_dest = os.path.join(dir_pkgs, pkg.replace('.',''))
        if fold_src != fold_dest:
            os.rename(fold_src, fold_dest)


print("~~~ End of 1_download_pkgs.py ~~~")