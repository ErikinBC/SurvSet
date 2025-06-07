"""
Contains the package name and respective dataset names.

Note that the key has to match the name of the class in the datasets.py file, and the values are dicts whose keys are the names of the process functions we want to call, and the values are the filenames. The latter of these has to align with the ACTUAL names tabt are found in the R package or the RData file output.
"""

# Load the processing classes
from .datasets import AdapEnetClass, AF, asaur, bujar, coin, coxph, CoxRidge, \
    Ecdat, EHA, frailtySurv, hdnom, iBST, invGauss, JM, joineR, jointCox, \
    MASS, mlr3proba, NestedCohort, pec, penalized, plsRcox, \
    randomForestSRC, RCASPAR, RcmdrPluginsurvival, relsurv, RISCA, RobustAFT, rpart, \
    smcure, smoothHR, spBayesSurv, survival, survJamdadata, THdata	, timereg


# Store in a dict
di_Rprocess = {
    AdapEnetClass: [
        ('process_MCLcleaned','MCLcleaned')
    ],
    AF: [
        ('process_rott2','rott2')
    ],
    asaur: [
        ('process_hepatoCellular','hepatoCellular'),
        ('process_pharmacoSmoking','pharmacoSmoking'),
        ('process_prostateSurvival','prostateSurvival')
    ],
    bujar: [
        ('process_chop','chop')
    ],
    coin: [
        ('process_glioma', 'glioma')
    ], 
    coxph: [
        ('process_breast', 'breast')
    ],
    CoxRidge: [
        ('process_ova', 'ova')
    ], 
    Ecdat: [
        ('process_UnempDur', 'UnempDur'),
        ('process_Unemployment', 'Unemployment')
    ], 
    EHA: [
        ('process_scania', 'scania'),
        ('process_oldmort', 'oldmort')
    ], 
    frailtySurv: [
        ('process_hdfail', 'hdfail')
    ], 
    hdnom: [
        ('process_smarto', 'smarto')
    ], 
    iBST: [
        ('process_burn', 'burn')
    ], 
    invGauss: [
        ('process_oropha', 'd.oropha.rec')
    ], 
    JM: [
        ('process_aids', 'aids')
    ], 
    joineR: [
        ('process_heartvalve', 'heart.valve'),
        ('process_epileptic', 'epileptic')
    ], 
    jointCox: [
        ('process_dataOvarian1', 'dataOvarian1')
    ], 
    MASS: [
        ('process_aids2', 'Aids2'),
        ('process_melanoma', 'Melanoma')
    ], 
    mlr3proba: [
        ('process_grace', 'grace'),
        ('process_actg', 'actg')
    ], 
    NestedCohort: [
        ('process_zinc', 'zinc')
    ], 
    pec: [
        ('process_Pbc3', 'Pbc3'),
        ('process_cost', 'cost'),
        ('process_GBSG2', 'GBSG2')
    ], 
    penalized: [
        ('process_nki70', 'nki70')
    ], 
    plsRcox: [
        ('process_microcensurei70', 'micro.censure')
    ], 
    randomForestSRC: [
        ('process_follic', 'follic'),
        ('process_vdv', 'vdv')
    ], 
    RCASPAR: [
        ('process_Bergamaschi', 'Bergamaschi')
    ], 
    RcmdrPluginsurvival: [
        ('process_Dialysis', 'Dialysis'),
        ('process_Rossi', 'Rossi')
    ], 
    relsurv: [
        ('process_rdata', 'rdata')
    ],
    RISCA: [
        ('process_DIVAT1', 'dataDIVAT1'),
        ('process_DIVAT2', 'dataDIVAT2'),
        ('process_DIVAT3', 'dataDIVAT3')
    ], 
    RobustAFT: [
        ('process_Z243', 'Z243')
    ], 
    rpart: [
        ('process_stagec', 'stagec')
    ], 
    smcure: [
        ('process_e1684', 'e1684')
    ], 
    smoothHR: [
        ('process_whas500', 'whas500')
    ], 
    spBayesSurv: [
        ('process_LeukSurv', 'LeukSurv')
    ], 
    survival: [
        ('process_cancer', 'cancer'),
        ('process_cgd', 'cgd'),
        ('process_colon', 'colon'),
        ('process_flchain', 'flchain'),
        ('process_heart', 'heart'),
        ('process_mgus', 'mgus'),
        ('process_ovarian', 'ovarian'),
        ('process_pbc', 'pbc'),
        ('process_retinopathy', 'retinopathy'),
        ('process_veteran', 'veteran'),
        ('process_nwtco', 'nwtco'),
    ], 
    survJamdadata: [
        ('process_gse4335', 'gse4335'),
        ('process_gse1992', 'gse1992'),
        ('process_gse3143', 'gse3143')
    ], 
    THdata: [
        ('process_wpbc', 'wpbc')
    ], 
    timereg: [
        ('process_TRACE', 'TRACE'),
        ('process_csl', 'csl'),
        ('process_diabetes', 'diabetes')
    ]
}