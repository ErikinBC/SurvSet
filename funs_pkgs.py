# Dictionary of dataset references
di_ref = {
    # AdapEnetClass
    'MCLcleaned':'https://rdrr.io/cran/AdapEnetClass/man/MCLcleaned.html',
    # AF
    'rott2':'https://rdrr.io/cran/AF/man/rott2.html',
    # asaur
    'hepatoCellular':'https://rdrr.io/cran/asaur/man/hepatoCellular.html',
    'pharmacoSmoking':'https://rdrr.io/cran/asaur/man/pharmacoSmoking.html',
    'prostateSurvival':'https://rdrr.io/cran/asaur/man/prostateSurvival.html',
    # bujar
    'chop':'https://rdrr.io/cran/bujar/man/chop.html',
    # coin
    'glioma':'https://rdrr.io/cran/coin/man/glioma.html',
    # CoxRidge
    'glioma':'https://rdrr.io/cran/CoxRidge/man/ova.html',
    # coxphf
    'breast':'https://rdrr.io/cran/coxphf/man/breast.html',
    # Ecdat
    'UnempDur':'https://rdrr.io/cran/Ecdat/man/UnempDur.html',
    'Unemployment':'https://rdrr.io/cran/Ecdat/man/Unemployment.html',
    # EHA
    'scania':'https://www.rdocumentation.org/packages/eha/versions/2.9.0/topics/scania',
    'oldmort':'https://www.rdocumentation.org/packages/eha/versions/2.9.0/topics/oldmort',
    # frailtySurv
    'hdfail':'https://www.rdocumentation.org/packages/frailtySurv/versions/1.3.7/topics/hdfail',
    # hdnom
    'smarto':'https://rdrr.io/cran/hdnom/man/smarto.html',
    # IPWsurvival
    'DIVAT':'https://rdrr.io/cran/IPWsurvival/man/DIVAT.html',
    # JM
    'aids':'https://www.rdocumentation.org/packages/JM/versions/1.5-1/topics/aids',
    # joineR
    'heartvalve':'https://rdrr.io/cran/joineR/man/heart.valve.html',
    'epileptic':'https://rdrr.io/cran/joineR/man/epileptic.html',
    # jointCox
    'dataOvarian1':'https://rdrr.io/cran/joint.Cox/man/dataOvarian1.html',
    # MASS
    'Aids2':'https://stat.ethz.ch/R-manual/R-devel/library/MASS/html/Aids2.html',
    'Melanoma':'https://stat.ethz.ch/R-manual/R-devel/library/MASS/html/Melanoma.html',
    # NestedCohort
    'zinc':'https://rdrr.io/cran/NestedCohort/man/zinc.html',
    # pec
    'Pbc3':'https://rdrr.io/cran/pec/man/Pbc3.html',
    'cost':'https://rdrr.io/cran/pec/man/cost.html',
    'GBSG2':'https://rdrr.io/cran/pec/man/GBSG2.html',
    # penalized
    'nki70':'https://rdrr.io/cran/penalized/man/nki70.html',
    # randomForestSRC
    'follic':'https://rdrr.io/cran/randomForestSRC/man/follic.html',
    'vdv':'https://rdrr.io/cran/randomForestSRC/man/vdv.html',
    # RCASPAR
    'Bergamaschi':'https://rdrr.io/bioc/RCASPAR/man/Bergamaschi.html',
    # RcmdrPlugin
    # relsurv
    # RobustAFT
    # rpart
    # smcure
    # smoothHR
    # spBayesSurv
    # survival
    'cancer':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/lung.html', 
    'cgd':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cgd.html',
    'colon':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/colon.html',
    'flchain':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/flchain.html',
    'heart':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/heart.html',
    'mgus':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/mgus.html',
    'ovarian':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/ovarian.html',
    'pbc':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/pbc.html',
    'retinopathy':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/retinopathy.html',
    'veteran':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/veteran.html',
    'nwtco':'https://stat.ethz.ch/R-manual/R-devel/library/survival/html/nwtco.html',
    # survJamda
    # TH
    # timereg
    }

# Contains list of packages that have data
di_pkgs = {'joineR':'https://cran.r-project.org/src/contrib/Archive/joineR/joineR_1.2.5.tar.gz', # 2020-02-08
    'survival':'https://cran.r-project.org/src/contrib/Archive/survival/survival_3.1-11.tar.gz', #2020-04-10 
    'MASS':'https://cran.r-project.org/src/contrib/Archive/MASS/MASS_7.3-51.6.tar.gz', #2020-04-26 12:32
    'coxphf':'https://cran.r-project.org/src/contrib/Archive/coxphf/coxphf_1.13.tar.gz', #2018-03-03
    'timereg':'https://cran.r-project.org/src/contrib/Archive/timereg/timereg_1.9.5.tar.gz', #2020-05-27 
    'eha':'https://cran.r-project.org/src/contrib/Archive/eha/eha_2.8.1.tar.gz', #2020-04-01  
    'RobustAFT':'https://cran.r-project.org/src/contrib/Archive/RobustAFT/RobustAFT_1.4-4.tar.gz', #2019-07-18 
    'AdapEnetClass':'https://cran.r-project.org/src/contrib/Archive/AdapEnetClass/AdapEnetClass_1.1.tar.gz', #2014-10-19 22:22
    'bujar':'https://cran.r-project.org/src/contrib/Archive/bujar/bujar_0.2-8.tar.gz', #2020-06-02 
    'survJamda.data':'https://cran.r-project.org/src/contrib/Archive/survJamda.data/survJamda.data_1.0.1.tar.gz', #2012-10-29
    'CoxRidge':'https://cran.r-project.org/src/contrib/Archive/CoxRidge/CoxRidge_0.9.2.tar.gz', #2015-02-27 
    'penalized':'https://cran.r-project.org/src/contrib/Archive/penalized/penalized_0.9-50.1.tar.gz', #2018-06-30
    'rpart':'https://cran.r-project.org/src/contrib/Archive/rpart/rpart_4.1-15.tar.gz', #2019-04-12
    'TH.data':'https://cran.r-project.org/src/contrib/Archive/TH.data/TH.data_1.0-10.tar.gz', #2019-01-21
    'randomForestSRC':'https://cran.r-project.org/src/contrib/Archive/randomForestSRC/randomForestSRC_2.10.1.tar.gz', #2021-02-10 
    'coin':'https://cran.r-project.org/src/contrib/Archive/coin/coin_1.3-1.tar.gz', #2019-08-28
    'frailtySurv':'https://cran.r-project.org/src/contrib/Archive/frailtySurv/frailtySurv_1.3.6.tar.gz', #2019-04-20 
    'spBayesSurv':'https://cran.r-project.org/src/contrib/Archive/spBayesSurv/spBayesSurv_1.1.4.tar.gz', #2020-02-23 
    'NestedCohort':'https://cran.r-project.org/src/contrib/Archive/NestedCohort/NestedCohort_1.1-3.tar.gz', #2013-02-07
    'joint.Cox':'https://cran.r-project.org/src/contrib/Archive/joint.Cox/joint.Cox_3.8.tar.gz', #2020-05-25
    'RCASPAR':'https://www.bioconductor.org/packages/3.14/bioc/src/contrib/Archive/RCASPAR/RCASPAR_1.39.0.tar.gz',  #2021-12-01 
    'IPWsurvival':'https://cran.r-project.org/src/contrib/Archive/IPWsurvival/IPWsurvival_0.5.tar.gz', #2017-03-24 
    'hdnom':'https://cran.r-project.org/src/contrib/Archive/hdnom/hdnom_5.0.tar.gz', #2018-05-14 
    'relsurv':'https://cran.r-project.org/src/contrib/Archive/relsurv/relsurv_2.2-3.tar.gz', #2018-11-30 
    'pec':'https://cran.r-project.org/src/contrib/Archive/pec/pec_2020.11.17.tar.gz', #2020-11-16 
    'JM':'https://cran.r-project.org/src/contrib/Archive/JM/JM_1.4-7.tar.gz', #2017-06-27 
    'asaur':'https://cran.r-project.org/src/contrib/Archive/asaur/asaur_0.44.tar.gz', #2016-02-17 
    'AF':'https://cran.r-project.org/src/contrib/Archive/AF/AF_0.1.4.tar.gz', #2017-02-11
    'Ecdat':'https://cran.r-project.org/src/contrib/Archive/Ecdat/Ecdat_0.3-7.tar.gz', #2020-02-10
    'smcure':'https://cran.r-project.org/src/contrib/Archive/smcure/smcure_1.0.tar.gz', #2012-02-11 
    'smoothHR':'https://cran.r-project.org/src/contrib/smoothHR_1.0.3.tar.gz', #2021-10-07
    'plsRcox':'https://cran.r-project.org/src/contrib/plsRcox_1.7.6.tar.gz', #2021-03-19
    'mlr3proba':'https://cran.r-project.org/src/contrib/mlr3proba_0.4.3.tar.gz', #2022-01-22
    'sodavis':'https://cran.r-project.org/src/contrib/sodavis_1.2.tar.gz'} #2018-05-13
