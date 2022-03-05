# Load modules
import os
import gzip
import rdata
import shutil
import tarfile
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
from zipfile import ZipFile
from urllib.request import urlretrieve

# Remove annoying warning from load_rda
lst_warnings = ['Unknown encoding. Assumed ASCII.', 'Missing constructor for R class "Date". The underlying R object is returned instead.', 'Missing constructor for R class "impute". The underlying R object is returned instead.']
lst_warnings += ['Tag not implemented for type RObjectType.%s and ignored' % k for k in ['STR', 'CHAR', 'REAL', 'VEC']]
for warning in lst_warnings:
    warnings.filterwarnings('ignore', message=warning)

# Find where the funs_support folder lives
def find_dir_base():
    dir_base = Path(__file__).parent
    return dir_base

# Make a folder if it does not exist
def makeifnot(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    else:
        print('Path already exists')

def test_fun(path):
    print(path)

# Get min and max of a Series
def get_min_max(x):
    return pd.DataFrame({'mi':x.min(), 'mx':x.max()}, index=[0])

# stringr like
def str_subset(x, pat, regex=True):
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    z = x[x.str.contains(pat, regex=regex)]
    z.reset_index(drop=True, inplace=True)
    return z


# stringr like
def str_detect(x, pat, regex=True):
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    z = x.str.contains(pat, regex=regex)
    z.reset_index(drop=True, inplace=True)
    return z


# Load an RDA file
def load_rda(fold, fn):
    path = os.path.join(fold, fn)
    assert os.path.exists(path), 'Cannot find path!'
    parsed = rdata.parser.parse_file(path)
    converted = rdata.conversion.convert(parsed)
    fn_rda = '.'.join(fn.split('.')[:-1])
    df = converted[fn_rda]
    # This is how missing values are encoded
    if isinstance(df, pd.DataFrame):
        df.replace(-2147483648, np.nan, inplace=True)
    return df

# Download zipped folder
def download_zip(url, fold):
    fn_url = url.split('/')[-1]
    path_write = os.path.join(fold, fn_url)
    path_unzip = path_write.replace('.zip','')
    exists = os.path.exists(path_write) or os.path.exists(path_unzip)
    if not exists:
        urlretrieve(url=url, filename=path_write)
        with ZipFile(path_write, 'r') as zip:
            zip.extractall(path_unzip)
        os.remove(path_write)
    else:
        print('Folder/zip already exists')

# Download file if it does not exist
def download_csv(url, fold):
    fn_csv = get_fn_url(url)[0]
    # Extract filename from url
    path_write = os.path.join(fold, fn_csv)
    if not os.path.exists(path_write):
        urlretrieve(url=url, filename=path_write)
    else:
        print('CSV file already exists')

# Extract filename from the url
def get_fn_url(url):
    lst = pd.Series(url).str.split('/')
    fn = lst.apply(lambda x: x[-1])
    fn = fn.str.replace('\\.csv$','',regex=True)
    fn = fn + '.csv'
    return fn

# Make an unzipped copy of a file
def unzip(path):
    path_new = path.replace('.gz','')
    if path_new != path:
        with gzip.open(path, 'rb') as f_in:
            with open(path_new, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(path)


# Extract files from a specific tar.gz file
def untar(path_tar, path_write, path_extract):
    tmp_tar = tarfile.open(path_tar)
    subdir_and_files = [tarinfo for tarinfo in tmp_tar.getmembers() if tarinfo.name.startswith(path_extract) ]
    tmp_tar.extractall(members=subdir_and_files, path=path_write)
    tmp_tar.close()



