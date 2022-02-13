import os
import gzip
import shutil
import tarfile
import pandas as pd

# Make a folder if it does not exist
def makeifnot(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


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


# # Function to count categorical features
# bin_count <- function(df) {
#   df <- as.data.frame(df)
#   idx.u <- apply(df,2,function(cc) length(unique(cc)))
#   idx.leq <- which(idx.u <= 12)
#   if (length(idx.leq) > 0) {
#     print(apply(df[,idx.leq,drop=F],2,table))
#     propv <- apply(df[,which(idx.u <= 12),drop=F],2,function(cc) min(prop.table(table(cc))) )
#     if ( any(propv < 0.05) ) {
#       print('The following features have a class imbalance < 5%')
#       print(propv[propv < 0.05])
#     }  
#   }
# }
