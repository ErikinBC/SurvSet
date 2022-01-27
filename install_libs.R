# Script to install specific versions of each needed package
args = commandArgs(trailingOnly=T)
fold_pkgs = args[1]
mirror = args[2]
print(sprintf('fold_pkgs=%s, mirror=%s',fold_pkgs, mirror))
# fold_pkgs='pkgs';mirror='https://utstat.toronto.edu/cran'


################################
# ---- (1) SET UP FOLDERS ---- #

if (!dir.exists(fold_pkgs)) {
    print(sprintf('Making folder %s for local packages',fold_pkgs))
    dir.create(fold_pkgs)
} else {
    print(sprintf('%s folder already exists',fold_pkgs))
}
dir_base = getwd()
dir_pkgs = file.path(dir_base, fold_pkgs)

# Add pkgs to .libLoc
.libPaths(dir_pkgs)
libs = .libPaths()
libs_rest = setdiff(libs, dir_pkgs)

# Determine which packages have already been installed
pkgs_folder = rownames(installed.packages(lib.loc=dir_pkgs))
pkgs_rest = rownames(installed.packages(lib.loc=libs_rest))
pkgs_all = unique(c(pkgs_folder, pkgs_rest))


##################################
# ---- (2) INSTALL PACKAGES ---- #

# (i) Remotes is needed to for specific package version
if (!('remotes' %in% pkgs_all)) {
    install.packages('remotes', lib=dir_pkgs, repos=mirror)
}

# (ii) List of packages and versions
lst_pkgs = 
list(
    joineR='https://cran.r-project.org/src/contrib/Archive/joineR/joineR_1.2.5.tar.gz', # 2020-02-08
    survival='https://cran.r-project.org/src/contrib/Archive/survival/survival_3.1-11.tar.gz', #2020-04-10 
    MASS='https://cran.r-project.org/src/contrib/Archive/MASS/MASS_7.3-51.6.tar.gz', #2020-04-26 12:32
    coxphf='https://cran.r-project.org/src/contrib/Archive/coxphf/coxphf_1.13.tar.gz', #2018-03-03
    timereg='https://cran.r-project.org/src/contrib/Archive/timereg/timereg_1.9.5.tar.gz', #2020-05-27 
    eha='https://cran.r-project.org/src/contrib/Archive/eha/eha_2.8.1.tar.gz', #2020-04-01  
    RobustAFT='https://cran.r-project.org/src/contrib/Archive/RobustAFT/RobustAFT_1.4-4.tar.gz', #2019-07-18 
    AdapEnetClass='https://cran.r-project.org/src/contrib/Archive/AdapEnetClass/AdapEnetClass_1.1.tar.gz', #2014-10-19 22:22
    bujar='https://cran.r-project.org/src/contrib/Archive/bujar/bujar_0.2-8.tar.gz', #2020-06-02 
    survJamda.data='https://cran.r-project.org/src/contrib/Archive/survJamda.data/survJamda.data_1.0.1.tar.gzz', #2012-10-29
    CoxRidge='https://cran.r-project.org/src/contrib/Archive/CoxRidge/CoxRidge_0.9.2.tar.gz', #2015-02-27 
    penalized='https://cran.r-project.org/src/contrib/Archive/penalized/penalized_0.9-50.1.tar.gz', #2018-06-30
    rpart='https://cran.r-project.org/src/contrib/Archive/rpart/rpart_4.1-15.tar.gz', #2019-04-12
    TH.data='https://cran.r-project.org/src/contrib/Archive/TH.data/TH.data_1.0-10.tar.gz', #2019-01-21
    randomForestSRC='https://cran.r-project.org/src/contrib/Archive/randomForestSRC/randomForestSRC_2.10.1.tar.gz', #2021-02-10 
    coin='https://cran.r-project.org/src/contrib/Archive/coin/coin_1.3-1.tar.gz', #2019-08-28
    frailtySurv='https://cran.r-project.org/src/contrib/Archive/frailtySurv/frailtySurv_1.3.6.tar.gz', #2019-04-20 
    spBayesSurv='https://cran.r-project.org/src/contrib/Archive/spBayesSurv/spBayesSurv_1.1.4.tar.gz', #2020-02-23 
    NestedCohort='https://cran.r-project.org/src/contrib/Archive/NestedCohort/NestedCohort_1.1-3.tar.gz', #2013-02-07
    joint.Cox='https://cran.r-project.org/src/contrib/Archive/joint.Cox/joint.Cox_3.8.tar.gz', #2020-05-25
    RCASPAR='https://www.bioconductor.org/packages/3.14/bioc/src/contrib/Archive/RCASPAR/RCASPAR_1.39.0.tar.gz',  #2021-12-01 
    IPWsurvival='https://cran.r-project.org/src/contrib/Archive/IPWsurvival/IPWsurvival_0.5.tar.gz', #2017-03-24 
    hdnom='https://cran.r-project.org/src/contrib/Archive/hdnom/hdnom_5.0.tar.gz', #2018-05-14 
    relsurv='https://cran.r-project.org/src/contrib/Archive/relsurv/relsurv_2.2-3.tar.gz', #2018-11-30 
    pec='https://cran.r-project.org/src/contrib/Archive/pec/pec_2020.11.17.tar.gz', #2020-11-16 
    JM='https://cran.r-project.org/src/contrib/Archive/JM/JM_1.4-7.tar.gz', #2017-06-27 
    asaur='https://cran.r-project.org/src/contrib/Archive/asaur/asaur_0.44.tar.gz', #2016-02-17 
    AF='https://cran.r-project.org/src/contrib/Archive/AF/AF_0.1.4.tar.gz', #2017-02-11
    Ecdat='https://cran.r-project.org/src/contrib/Archive/Ecdat/Ecdat_0.3-7.tar.gz', #2020-02-10
    smcure='https://cran.r-project.org/src/contrib/Archive/smcure/smcure_1.0.tar.gz' #2012-02-11 
    )


# Install those that are needed
all_packages = names(lst_pkgs)
match_rest = intersect(all_packages, pkgs_rest)
match_folder = intersect(all_packages, pkgs_folder)
match_all = unique(c(match_rest, match_folder))
needed_packages = setdiff(all_packages, match_all)
n_needed = length(needed_packages)
print(sprintf('%i packages need to be installed (%i found in rest, %i fold in folder)',n_needed,length(match_rest),length(match_folder)))
vec_dep = c('Depends') #,'Imports','LinkingTo'

j = 0
for (package in needed_packages) {
    j = j + 1
    package_url = lst_pkgs[[package]]
    version = strsplit(package_url, paste0(package,'_'))[[1]][2]
    version = gsub('.tar.gz','',version)
    print(sprintf('Installing package = %s (%i of %i)',package, j, n_needed))
    install.packages(pkgs=package, repos=mirror)
    # remotes::install_version(package=package, version=version, dependencies=vec_dep, repos=mirror) 
    # install.packages(pkgs=, lib=dir_pkgs, repos=mirror, dependencies=c('Depends','Imports','LinkingTo'))
}


print("~~~ End of install_libs.R ~~~")