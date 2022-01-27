# Script to grab datasets from specific packages

########################
# ---- (1) SET UP ---- #

# (i) Files will be downloaded in fold_pkgs
# (ii) mirror defines the CRAN repo to download from
args = commandArgs(trailingOnly=T)
fold_pkgs = args[1]
mirror = args[2]
print(sprintf('fold_pkgs=%s, mirror=%s', fold_pkgs, mirror))
# fold_pkgs='pkgs';mirror='https://utstat.toronto.edu/cran'

# (iii) Utility functions and pacage list
source('funs_support.R')
source('funs_pkgs.R')

# (iv) Folder to write into
dir_base = getwd()
dir_pkgs = file.path(dir_base, fold_pkgs)
makeifnot(dir_pkgs)


###################################
# ---- (2) DOWNLOAD PACKAGES ---- #

# (i) Find which have not been downloaded
all_pkgs = names(lst_pkgs)
existing_pkgs = list.files(dir_pkgs)
n_existing = length(existing_pkgs)
needed_pkgs = setdiff(all_pkgs, existing_pkgs)
n_pkgs = length(needed_pkgs)
print(sprintf('%i packages need to be installed (%i fold in folder)',n_pkgs,n_existing))

# (ii) Download, extract, remove, and unzip
j = 0
for (pkg in needed_pkgs) {
    j = j + 1
    url_pkg = lst_pkgs[[pkg]]
    fn_pkg = strsplit(url_pkg, '/')[[1]]
    fn_pkg = fn_pkg[length(fn_pkg)]
    dest_pkg = file.path(dir_pkgs, fn_pkg)
    print(sprintf('Downloading package = %s (%i of %i)', pkg, j, n_pkgs))
    download.file(url_pkg, destfile=dest_pkg)
    # Extract only the data folder
    fold_data = file.path(dir_pkgs, pkg, 'data')
    if (!dir.exists(fold_data)) {
        untar(tarfile=dest_pkg, files=paste(pkg,'data',sep='/'), exdir=dir_pkgs)
    }
    stopifnot(dir.exists(fold_data))
    # Remove the tar file
    file.remove(dest_pkg)
}


print("~~~ End of download_pkgs.R ~~~")