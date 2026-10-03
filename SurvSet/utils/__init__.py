"""
Contains utility parameters/paths shared across the SurvSet package.
"""

# Define the name of the csv which stores the dataset information
fn_df_ds = 'df_ds.csv'

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
    'ova':'https://rdrr.io/cran/CoxRidge/man/ova.html',
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
    # Hosmer
    'uis':'https://github.com/graemeleehickey/hosmer-lemeshow/blob/master/edition2/uis.txt',
    'FRTCS':'https://github.com/graemeleehickey/hosmer-lemeshow/blob/master/edition2/FRTCS%20.txt',
    # iBST
    'burn':'https://rdrr.io/cran/iBST/man/burn.html',
    # invGauss
    'd.oropha.rec':'https://rdrr.io/cran/invGauss/man/d.oropha.rec.html',
    # # IPWsurvival
    # 'DIVAT':'https://rdrr.io/cran/IPWsurvival/man/DIVAT.html',
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
    # mlr3proba
    'actg':'https://search.r-project.org/CRAN/refmans/mlr3proba/html/actg.html',
    'grace':'https://search.r-project.org/CRAN/refmans/mlr3proba/html/grace.html',
    # NestedCohort
    'zinc':'https://rdrr.io/cran/NestedCohort/man/zinc.html',
    # openml
    'phpl04K8a':'https://www.openml.org/d/1245',
    # pec
    'Pbc3':'https://rdrr.io/cran/pec/man/Pbc3.html',
    'cost':'https://rdrr.io/cran/pec/man/cost.html',
    'GBSG2':'https://rdrr.io/cran/pec/man/GBSG2.html',
    # penalized
    'nki70':'https://rdrr.io/cran/penalized/man/nki70.html',
    # plsRcox
    'micro.censure':'https://rdrr.io/cran/plsRcox/man/micro.censure.html',
    # princton
    'divorce':'https://data.princeton.edu/wws509/datasets/#divorce',
    # randomForestSRC
    'follic':'https://rdrr.io/cran/randomForestSRC/man/follic.html',
    'vdv':'https://rdrr.io/cran/randomForestSRC/man/vdv.html',
    # RCASPAR
    'Bergamaschi':'https://rdrr.io/bioc/RCASPAR/man/Bergamaschi.html',
    # RcmdrPlugin
    'Dialysis':'https://rdrr.io/cran/RcmdrPlugin.survival/man/Dialysis.html',
    'Rossi':'https://rdrr.io/cran/RcmdrPlugin.survival/man/Rossi.html',
    # Reddy
    'NSBCD':'https://dmkd.cs.vt.edu/projects/survival/data',
    'AML_Bull':'https://dmkd.cs.vt.edu/projects/survival/data',
    'DBCD':'https://dmkd.cs.vt.edu/projects/survival/data',   
    'DLBCL':'https://dmkd.cs.vt.edu/projects/survival/data',
    # relsurv
    'rdata':'https://www.rdocumentation.org/packages/relsurv/versions/2.2-6/topics/rdata',
    # RISCA
    'dataDIVAT1':'https://rdrr.io/cran/RISCA/man/dataDIVAT1.html',
    'dataDIVAT2':'https://rdrr.io/cran/RISCA/man/dataDIVAT2.html',
    'dataDIVAT3':'https://rdrr.io/cran/RISCA/man/dataDIVAT3.html',
    # RobustAFT
    'Z243':'https://www.rdocumentation.org/packages/RobustAFT/versions/1.4-5/topics/Z243',
    # rpart
    'stagec':'https://rdrr.io/cran/rpart/man/stagec.html',
    # smcure
    'e1684':'https://www.rdocumentation.org/packages/smcure/versions/2.0/topics/e1684',
    # smoothHR
    'whas500':'https://rdrr.io/cran/smoothHR/man/whas500.html',
    # spBayesSurv
    'LeukSurv':'https://rdrr.io/cran/spBayesSurv/man/LeukSurv.html',
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
    # survJamda.data
    'gse4335':'https://www.rdocumentation.org/packages/survJamda.data/versions/1.0.2/topics/gse4335',
    'gse3143':'https://www.rdocumentation.org/packages/survJamda.data/versions/1.0.2/topics/gse3143',
    'gse1992':'https://www.rdocumentation.org/packages/survJamda.data/versions/1.0.2/topics/gse1992',
    # TH
    'wpbc':'https://rdrr.io/cran/TH.data/man/wpbc.html',
    # timereg
    'TRACE':'https://rdrr.io/cran/timereg/man/TRACE.html',
    'csl':'https://rdrr.io/cran/timereg/man/csl.html',
    'diabetes':'https://rdrr.io/cran/timereg/man/diabetes.html',
    # vanderbilt
    'support2':'https://hbiostat.org/data/repo/Csupport2.html',
    'prostate':'https://hbiostat.org/data/repo/Cprostate.html',
    'Framingham':'https://math.montana.edu/shancock/courses/stat439/R/Week4-GLMIntro-Framingham.html',
    'rhc':'https://hbiostat.org/data/repo/rhc.html',
    'acath':'https://hbiostat.org/data/repo/Cacath.html',
    'vlbw':'https://hbiostat.org/data/repo/Cvlbw.html',
    }


# Application field (domain) and sub-field of each dataset, see GitHub issue #12
# Added to SurvLoader().df_ds so datasets can be filtered by field
di_domain = {
    # Oncology
    'prostateSurvival': ('Oncology', 'Prostate cancer'),
    'nwtco': ('Oncology', 'Wilms tumour (paediatric)'),
    'rott2': ('Oncology', 'Breast cancer (Rotterdam)'),
    'LeukSurv': ('Oncology', 'Acute myeloid leukaemia'),
    'colon': ('Oncology', 'Colon cancer adjuvant trial'),
    'dataOvarian1': ('Oncology', 'Ovarian cancer relapse (gene expression)'),
    'GBSG2': ('Oncology', 'Breast cancer (German BCSG trial)'),
    'follic': ('Oncology', 'Follicular lymphoma'),
    'prostate': ('Oncology', 'Prostate cancer'),
    'phpl04K8a': ('Oncology', 'Lung adenocarcinoma (Shedden et al., gene expression)'),
    'zinc': ('Oncology', 'Esophageal cancer & tissue zinc (Linxian trial)'),
    'chop': ('Oncology', 'DLBCL treated with CHOP (gene expression)'),
    'ova': ('Oncology', 'Ovarian cancer'),
    'DBCD': ('Oncology', 'Breast cancer (Dutch, gene expression)'),
    'e1684': ('Oncology', 'Melanoma (ECOG 1684)'),
    'mgus': ('Oncology', 'Monoclonal gammopathy (MGUS)'),
    'DLBCL': ('Oncology', 'Diffuse large B-cell lymphoma (gene expression)'),
    'cancer': ('Oncology', 'Lung cancer (NCCTG)'),
    'hepatoCellular': ('Oncology', 'Hepatocellular carcinoma'),
    'Melanoma': ('Oncology', 'Malignant melanoma'),
    'wpbc': ('Oncology', 'Breast cancer (Wisconsin prognostic)'),
    'd.oropha.rec': ('Oncology', 'Oropharyngeal carcinoma'),
    'gse3143': ('Oncology', 'Breast cancer (GSE3143, gene expression)'),
    'stagec': ('Oncology', 'Prostate cancer (stage C)'),
    'nki70': ('Oncology', 'Breast cancer (NKI 70-gene)'),
    'veteran': ('Oncology', 'Lung cancer (VA trial)'),
    'gse1992': ('Oncology', 'Breast cancer (GSE1992, gene expression)'),
    'micro.censure': ('Oncology', 'Rectal cancer (microsatellite allelotyping)'),
    'AML_Bull': ('Oncology', 'Acute myeloid leukaemia (Bullinger, gene expression)'),
    'NSBCD': ('Oncology', 'Breast cancer (Norway/Stanford, gene expression)'),
    'gse4335': ('Oncology', 'Breast cancer (GSE4335, gene expression)'),
    'breast': ('Oncology', 'Breast cancer'),
    'MCLcleaned': ('Oncology', 'Mantle cell lymphoma (gene expression)'),
    'Bergamaschi': ('Oncology', 'Breast cancer (gene expression)'),
    'vdv': ('Oncology', "Breast cancer (van 't Veer 70-gene, gene expression)"),
    'glioma': ('Oncology', 'Glioma (brain tumour)'),
    'ovarian': ('Oncology', 'Ovarian cancer trial'),
    # Cardiology
    'Framingham': ('Cardiology', 'Framingham heart study'),
    'smarto': ('Cardiology', 'Arterial disease (SMART)'),
    'acath': ('Cardiology', 'Coronary catheterisation (Duke)'),
    'FRTCS': ('Cardiology', 'Blood-pressure / hypertension'),
    'TRACE': ('Cardiology', 'Post-MI (TRACE)'),
    'grace': ('Cardiology', 'Acute coronary syndrome (GRACE)'),
    'heartvalve': ('Cardiology', 'Heart-valve surgery'),
    'whas500': ('Cardiology', 'Worcester heart-attack study'),
    # Transplant / Nephrology
    'Dialysis': ('Transplant / Nephrology', 'Dialysis patients'),
    'dataDIVAT1': ('Transplant / Nephrology', 'Kidney transplant (DIVAT)'),
    'dataDIVAT3': ('Transplant / Nephrology', 'Kidney transplant (DIVAT)'),
    'dataDIVAT2': ('Transplant / Nephrology', 'Kidney transplant (DIVAT)'),
    'heart': ('Transplant / Nephrology', 'Stanford heart transplant'),
    # Infectious disease
    'Aids2': ('Infectious disease', 'AIDS survival (Australia)'),
    'aids': ('Infectious disease', 'AIDS cohort'),
    'actg': ('Infectious disease', 'HIV trial (ACTG 320)'),
    'cgd': ('Infectious disease', 'Chronic granulomatous disease'),
    # Hepatology
    'csl': ('Hepatology', 'Liver cirrhosis (CSL)'),
    'Pbc3': ('Hepatology', 'Primary biliary cirrhosis (PBC3)'),
    'pbc': ('Hepatology', 'Primary biliary cirrhosis'),
    # Neurology
    'epileptic': ('Neurology', 'Epilepsy drug trial'),
    'cost': ('Neurology', 'Stroke (Copenhagen)'),
    # Critical care
    'support2': ('Critical care', 'Seriously-ill hospitalised (SUPPORT)'),
    'rhc': ('Critical care', 'Right-heart catheterisation'),
    'burn': ('Critical care', 'Burn-unit patients'),
    # Other clinical
    'flchain': ('Other clinical', 'Serum free light chain & mortality'),
    'uis': ('Other clinical', 'Drug-relapse (UIS)'),
    'vlbw': ('Other clinical', 'Very-low-birth-weight neonates'),
    'retinopathy': ('Other clinical', 'Diabetic retinopathy (survival)'),
    'diabetes': ('Other clinical', 'Diabetic retinopathy (timereg)'),
    'pharmacoSmoking': ('Other clinical', 'Smoking-cessation trial'),
    'Z243': ('Other clinical', 'Hospital length of stay, medical back problems (Swiss DRG 243)'),
    # Economics
    'UnempDur': ('Economics', 'Unemployment duration (US)'),
    'Unemployment': ('Economics', 'Unemployment spells'),
    # Social science
    'oldmort': ('Social science', 'Old-age mortality (demography)'),
    'divorce': ('Social science', 'Divorce / marriage duration'),
    'scania': ('Social science', 'Historical mortality (Scania)'),
    'Rossi': ('Social science', 'Criminal recidivism'),
    # Engineering / reliability
    'hdfail': ('Engineering / reliability', 'Hard-disk failure'),
    # Other / unspecified
    'rdata': ('Other / unspecified', 'Relative-survival example data (relsurv); provenance not documented'),
    }
