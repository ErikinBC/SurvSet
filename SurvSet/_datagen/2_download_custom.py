import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_custom', help='Name of the folder where the custom datasets will be downloaded to (default="pkgs"', default='custom')
args = parser.parse_args()
fold_custom = args.fold_custom
# fold_custom='custom'

# Load modules
import os
from urllib.request import urlretrieve
from funs_support import makeifnot, download_csv, download_zip, find_dir_base

# Folder to write into
dir_base = find_dir_base()
dir_custom = os.path.join(dir_base, fold_custom)
makeifnot(dir_custom)


# --- (1) Hosmer datasets --- #
fn_hosmer = ['FRTCS', 'uis']
dir_hosmer = os.path.join(dir_custom, 'hosmer')
makeifnot(dir_hosmer)
base_url = 'https://raw.githubusercontent.com/graemeleehickey/hosmer-lemeshow/master/edition2/%s.dat'
for fn in fn_hosmer:
    url = base_url % fn
    path = os.path.join(dir_hosmer,fn+'.csv')
    urlretrieve(url, path)

# --- (2) Lung Cancer --- #
# https://www.openml.org/d/1245
url = 'https://www.openml.org/data/get_csv/552598/phpl04K8a'
download_csv(url, dir_custom)

# --- (3) Reddy Datasets --- #
url = 'https://dmkd.cs.vt.edu/projects/survival/data/Gene_expression_data.zip'
download_zip(url, dir_custom)

# --- (4) Princeton GLM --- #
url = 'https://data.princeton.edu/wws509/datasets/divorce.dat'
path = os.path.join(dir_custom, url.split('/')[-1].replace('.dat','.csv'))
urlretrieve(url, path)

# --- (5) HBiostat --- #
dir_vanderbilt = os.path.join(dir_custom, 'vanderbilt')
makeifnot(dir_vanderbilt)
base = 'https://hbiostat.org/data/repo/'
fn_hb = ['support2csv.zip', 'prostate.xls', '2.20.Framingham.csv', 'rhc.csv', 'acath.xls.zip', 'vlbw.zip']
for fn in fn_hb:
    end = fn.split('.')[-1]
    url = os.path.join(base, fn)
    if end == 'zip':
        download_zip(url, dir_vanderbilt)
    elif end == 'xls':   
        path = os.path.join(dir_vanderbilt, fn) 
        urlretrieve(url, path)
    elif end == 'csv':
        download_csv(url, dir_vanderbilt)
    else:
        print('Unsure')

print('~~~ End of 2_download_custom.py ~~~')