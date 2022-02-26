rm(list=ls())

# Libraries for optparse
library(stringr,logical.return=F,warn.conflicts=F,quietly=T,verbose=F)
library(optparse,logical.return=F,warn.conflicts=F,quietly=T,verbose=F)

# Optional linux argument
option_list <- list(
  make_option('--dir_dataset',type='character',default=getwd(),help='Path to dataset directory to load files [default WD]'),
  make_option('--dir_output',type='character',default=getwd(),help='Path to output directory [default WD]')
);

# Parse and assign
opt <- parse_args(OptionParser(option_list=option_list))
dir.dataset <- opt$dir_dataset
dir.output <- opt$dir_output

# packageurl <- "http://cran.r-project.org/src/contrib/Archive/ggplot2/ggplot2_0.9.1.tar.gz"
# install.packages(packageurl, repos=NULL, type="source")

# Remaining packages
pckgs <- c('data.table','survival', 'MASS', 'data.table', 'forcats','stringr',
           'coxphf','timereg','dynsurv','eha','RobustAFT',
           'AdapEnetClass','bujar','survJamda.data','CoxRidge','penalized',
           'iC10','rpart', 'TH.data', 'randomForestSRC',
           'coin','frailtySurv','spBayesSurv','tdROC','condSURV',
           'joint.Cox','joineR','JM','NestedCohort','RCASPAR',
           'pec','Ecdat','popEpi','relsurv', 
           'IPWsurvival','hdnom','asaur','AF','Ecdat','smcure','joineR')
for (pp in pckgs) {
  ptest <- tryCatch(library(pp,character.only = T),error=function(e) NA)
  if (is.na(ptest)) {
    install.packages(pp)
  } else {
    library(pp,character.only = T)
  }
}



##################################################################
####### ------- BUILT IN SURVIVAL DATASETS ----------- ###########


##########################################################
####### ------- LIFELINES DATASETS ----------- ###########

dir.lifelines <- file.path(dir.dataset,'lifelines')

# --- (i) Anderson --- #
tmp.dat <- fread(file.path(dir.lifelines, 'anderson.csv'))
So.anderson <- with(tmp.dat, Surv(time=t, event=status))
X.anderson <- model.matrix(~sex+logWBC+Rx,data=tmp.dat)[,-1]
id.anderson <- seq(nrow(X.anderson))
cr.anderson <- NULL

# --- (ii) divorce --- #
tmp.dat <- fread(file.path(dir.lifelines,'divorce.raw'))
colnames(tmp.dat) <- c('id','heduc','heblack','mixed','years','div')
So.divorce <- with(tmp.dat, Surv(time = years, event=div))
X.divorce <- model.matrix(~heduc+heblack+mixed,data=tmp.dat)[,-1]
id.divorce <- as.numeric(as.factor(tmp.dat$id))
cr.divorce <- NULL

# --- (iii) kidney_transplat --- #
tmp.dat <- fread(file.path(dir.lifelines,'kidney_transplant.csv'))
So.kidney <- with(tmp.dat, Surv(time=time,event=death))
X.kidney <- as.matrix(tmp.dat[,-(1:2)])
id.kidney <- seq(nrow(X.kidney))
cr.kidney <- NULL

# --- (iv) larynx --- #
tmp.dat <- fread(file.path(dir.lifelines,'larynx.csv'))
So.larynx <- with(tmp.dat, Surv(time = time, event=death))
X.larynx <- as.matrix(tmp.dat[,-c(1,3)])
id.larynx <- seq(nrow(X.larynx))
cr.larynx <- NULL


###########################################################
####### ------- VANDERBILT DATASETS ----------- ###########

# http://biostat.mc.vanderbilt.edu/wiki/Main/DataSets

dir.vanderbilt <- file.path(dir.dataset, 'vanderbilt')

# --- (i) Support2 --- #
tmp <- fread(file.path(dir.vanderbilt, 'support2.csv'), drop=1) # (drop first column which is just the row index)
tmp.cn.char <- names(which(sapply(tmp,class)=='character'))
tmp[,(tmp.cn.char) := lapply(.SD, function(ll) ifelse(str_length(ll)==0,NA,ll)), .SDcols=tmp.cn.char]
tmp.na.mu <- apply(tmp, 2, function(cc) mean(is.na(cc)))
tmp.na.drop <- names(which(tmp.na.mu > 0.05))
tmp[, (tmp.na.drop) := NULL]
# median impute
tmp.na.impute <- names(which(tmp.na.mu < 0.05 & tmp.na.mu > 0))
tmp[, (tmp.na.impute) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=tmp.na.impute]
# Create design matrix
X.support2 <- model.matrix(~age + sex + dzgroup + dzclass + num.co + scoma + charges + avtisst +
                             race + hday + diabetes + dementia + ca + meanbp + wblc +  
                             hrt + resp + temp + crea + sod + adlsc, data=tmp)[,-1]
# Remove perfectly collinear factor
X.support2 <- X.support2[,colnames(X.support2) != 'dzgroupComa']
# Get the survival object
So.support2 <- with(tmp, Surv(time=d.time, event=death)) # For overall death
# So.support2 <- with(tmp, Surv(time=slos, event=hospdead)) # For death in hospital
id.support2 <- seq(nrow(X.support2))
cr.support2 <- NULL

# --- (ii) german breast cancer --- #
tmp <- data.table(read.delim(file.path(dir.vanderbilt, 'gbsg_ba_ca.dat')))
# matrix and surv
X.gbr <- model.matrix(~age+meno+size+factor(grade)+nodes+enodes+pgr+er+hormon,data=tmp)[,-1]
So.gbr <- with(tmp, Surv(time=X_t, event=X_d))
id.gbr <- as.numeric(as.factor(tmp$id))
cr.gbr <- NULL

# --- (iii) Byar & Greene prostate cancer data --- #
tmp <- fread(file.path(dir.vanderbilt, 'prostate.csv'))
tmp[, `:=` (pf=ifelse(pf=='normal activity','normal','in_bed'))]
tmp.na.mu <- apply(tmp, 2,function(ll) mean(is.na(ll)) )
tmp.na.impute <- names(which(tmp.na.mu > 0))
tmp[, (tmp.na.impute) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=tmp.na.impute]
X.byar <- model.matrix(~factor(stage)+rx+age+wt+pf+hx+sbp+dbp+hg+sz+sg+ap+bm, data=tmp)[,-1]
So.byar <- with(tmp, Surv(time=dtime, event = (status!='alive')) )
id.byar <- tmp$patno
cr.byar <- data.table(time=tmp$dtime,event=as.numeric(as.factor(tmp$status))-1)

# --- (iv) Framingham Heart --- #
tmp <- fread(file.path(dir.vanderbilt, 'Framingham.csv'))[order(id)]
tmp[, season := fct_recode(as.character(month),'fall'='9','fall'='10','fall'='11','winter'='12','winter'='1','winter'='2',
                           'spring'='3','spring'='4','spring'='5','summer'='6','summer'='7','summer'='8')]
tmp.na.mu <- apply(tmp, 2,function(ll) mean(is.na(ll)) )
tmp.na.impute <- names(which(tmp.na.mu > 0))
tmp[, (tmp.na.impute) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=tmp.na.impute]
X.framingham <- model.matrix(~factor(sex)+sbp+dbp+scl+age+bmi+season, data=tmp)[,-1]
So.framingham <- with(tmp, Surv(time=followup, event = chdfate) )
id.framingham <- tmp$id
cr.framingham <- NULL

# --- (v)  Right heart catheterization (RHC) dataset --- #
tmp.dat <- fread(file.path(dir.vanderbilt, 'rhc.csv'))
tmp.class <- sapply(tmp.dat,class)
tmp.class.char <- names(which(tmp.class == 'character'))
tmp.dat[, (tmp.class.char) := lapply(.SD, function(ll) ifelse(ll == 'NA',NA, ll) ), .SDcols=tmp.class.char]
tmp.na.cnt <- apply(tmp.dat,2,function(cc) sum(is.na(cc)) )
# Encode time
tmp.dat[, time := ifelse(death == 'Yes',dthdte - sadmdte, lstctdte - sadmdte)]
So.RHC <- with(tmp.dat, Surv(time=time, event=(death=='Yes')))

# Encode the features
tmp.dat[, `:=` (cat1 = fct_recode(cat1,'cancer'='Colon Cancer', 'cancer'='Lung Cancer', 'cancer'='MOSF w/Malignancy'),
                ca = fct_relevel(ca, c('No','Yes','Metastatic')))]

# Columns to drop
cn.drop <- c('V1','cat2','sadmdte','dschdte','dthdte','lstctdte','death','surv2md1',
              'das2d3pc','t3d30','dth30','ortho','trauma','adld3p','urin1','ptid','time')
X.RHC <- model.matrix(~.,data=tmp.dat[,-cn.drop,with=F])[,-1]
id.RHC <- as.numeric(as.factor(tmp.dat$ptid))
cr.RHC <- NULL

# --- (vi) Catheterization Coronary Artery Disease  --- #
tmp.dat <- fread(file.path(dir.vanderbilt, 'acath.csv'))
# Predict whether: Three Vessel or Left Main Disease by Cardiac Cath
mdl.tvdlm <- glm(tvdlm ~ sex + age + age^2 + sigdz,family=binomial,data=tmp.dat)
tmp.na.idx <- which(is.na(tmp.dat$tvdlm))
tmp.dat$tvdlm[tmp.na.idx] <- ifelse(predict(mdl.tvdlm,newdata=tmp.dat[tmp.na.idx])>0,1,0)

# Note that competent cholestoral prediction model cannot seem to be made
So.catheter <- Surv(time=tmp.dat$cad.dur, event=rep(1,nrow(tmp.dat)))
X.catheter <- model.matrix(~sex+age+sigdz+tvdlm,data=tmp.dat)[,-1]
id.catheter <- seq(nrow(X.catheter))
cr.catheter <- NULL

# --- (vii) ARI:  WHO ARI Multicentre Study of clinical signs and etiologic agents --- #
# require(rms)
# getHdata(ari)
# fwrite(x=data.table(Y.death=Y.death,ari),file=file.path(dir.vanderbilt,'ari.csv'))
tmp.dat <- fread(file.path(dir.vanderbilt,'ari.csv'))
# Remove any missing time
tmp.dat <- tmp.dat[!is.na(daydth)]
# Create the Surv object
So.ARI <- with(tmp.dat, Surv(time = daydth - min(daydth)+1, event = Y.death==3))
# Get impute any values with missing < 100, drop the rest
tmp.na.cnt <- apply(tmp.dat, 2, function(cc) sum(is.na(cc)))
tmp.na.cnt <- tmp.na.cnt[tmp.na.cnt>0]
tmp.na.fill <- names(which(tmp.na.cnt < 100))
tmp.na.drop <- names(which(tmp.na.cnt >= 100))
tmp.dat <- tmp.dat[,-tmp.na.drop,with=F]
# Impute the other
tmp.dat[, `:=` (wght = ifelse(is.na(wght),median(wght,na.rm=T),wght),
                wam = ifelse(is.na(wam),median(wam,na.rm=T),wam),
                bcpc = ifelse(bcpc==0,'zero','greater'),
                saogp = ifelse(is.na(saogp),as.numeric(names(which.max(table(tmp.dat$saogp)))),saogp),
                impcl = ifelse(is.na(impcl),names(which.max(table(tmp.dat$impcl))),as.character(impcl)),
                cprot = fct_recode(cprot, 'mild'='None','mild'='Cold,cough','pneumonia'='Pneumonia','pneumonia'='Severe pneumonia')) ]
tmp.dat[, bcpc := ifelse(is.na(bcpc),'zero',bcpc)]
# Create the multihot encoding for hlt
tmp.X.hlt <- matrix(NA,nrow=nrow(tmp.dat),ncol=2,dimnames = list(NULL,c('respir','chest')))
tmp.X.hlt[,'respir'] <- str_detect(tmp.dat$hlt,'Hy\\srespir')
tmp.X.hlt[,'chest'] <- str_detect(tmp.dat$hlt,'\\/chest')
tmp.X.hlt <- apply(tmp.X.hlt,2,as.numeric)
# Create the multihot encoding for impcl
tmp.X.impcl <- matrix(F,nrow=nrow(tmp.dat),ncol=3,dimnames = list(NULL,c('P','M','S')))
tmp.impcl <- tmp.dat$impcl
tmp.impcl <- as.character(fct_recode(tmp.impcl,'Z'='No P,S or M','Z'='No P,S,M-oth'))
tmp.impcl <- str_split(str_replace_all(str_remove_all(tmp.impcl,'\\sonly'),'\\sand\\s',','),'\\,')
for (ii in seq_along(tmp.impcl)) {
  cidx <- colnames(tmp.X.impcl) %in% tmp.impcl[[ii]]
  tmp.X.impcl[ii,cidx] <- T
}
tmp.X.impcl <- apply(tmp.X.impcl,2,as.numeric)

cn.keep1 <- c('biwt','hcir','wght','lgth','temp','hrat','country','age','rr','cprot','saogp','bcpc','waz','wam',
              'omph','conj','sickc','sickj','sickl')
cn.keep2 <- colnames(tmp.dat)[32:89]
cn.drop <- bin.count(tmp.dat[,32:89])
cn.keep2 <- setdiff(cn.keep2,names(which(cn.drop < 3.5/100)))
# Convert to factors
tmp.dat[, (cn.keep2) := lapply(.SD, as.character), .SDcols=cn.keep2]

# Now we create design matrix
X.ARI <- model.matrix(as.formula(str_c('~',str_c(c(cn.keep1, cn.keep2),collapse='+'))),data=tmp.dat)[,-1]
X.ARI <- cbind(X.ARI, tmp.X.hlt, tmp.X.impcl)

id.ARI <- as.numeric(as.factor(tmp.dat$stno))
cr.ARI <- data.table(time=tmp.dat$daydth, event=tmp.dat$Y.death)

# --- (viii) Very Low Birth Weight Infants Dataset --- #
tmp.dat <- fread(file.path(dir.vanderbilt, 'vlbw.csv'))
tmp.dat <- tmp.dat[!is.na(exit)] # Remove missing times
tmp.dat[, time := exit - birth]
tmp.dat <- tmp.dat[time > 0] # Remove non-sensical times
tmp.dat <- tmp.dat[race %in% c('white','black')] # Use only white/black
tmp.dat <- tmp.dat[dead == 1]# Subset to only patients who died
cn.char <- names(which(sapply(tmp.dat,class)=='character'))
tmp.dat[, (cn.char) := lapply(.SD,function(ss) ifelse(ss == 'NA',NA,ss)), .SDcols=cn.char]
tmp.na.cnt <- sort(apply(tmp.dat,2,function(cc) sum(is.na(cc))))
tmp.na.cnt <- tmp.na.cnt[tmp.na.cnt > 0]
# Drop if >10% missing
cn.drop <- names(which(tmp.na.cnt >= 60))
cn.fill <- names(which(tmp.na.cnt < 60))
tmp.dat <- tmp.dat[,-cn.drop,with=F]

tmp.dat[,cn.fill,with=F] %>% head
tmp.dat[, `:=` (gest = ifelse(is.na(gest),round(median(gest,na.rm=T)),gest),
                pltct = ifelse(is.na(pltct),round(median(pltct,na.rm=T)),pltct),
                apg1 = ifelse(is.na(apg1),round(median(apg1,na.rm=T)),apg1),
                lowph = ifelse(is.na(lowph),median(lowph,na.rm=T),lowph),
                pneumo = ifelse(is.na(pneumo),as.numeric(names(which.max(table(pneumo)))),pneumo),
                vent = ifelse(is.na(vent),as.numeric(names(which.max(table(vent)))),vent),
                pda = ifelse(is.na(pda),as.numeric(names(which.max(table(pda)))),pda),
                cld = ifelse(is.na(cld),as.numeric(names(which.max(table(cld)))),cld),
                sex = ifelse(is.na(sex),(names(which.max(table(sex)))),sex),
                inout = ifelse(is.na(inout),(names(which.max(table(inout)))),inout),
                delivery = ifelse(is.na(delivery),(names(which.max(table(delivery)))),delivery),
                race = ifelse(is.na(race),(names(which.max(table(race)))),race))]
# Create the model matrix
X.vlbw <- model.matrix(~lowph+pltct+race+bwt+gest+inout+twn+delivery+apg1+pneumo+pda+cld+year+sex,data=tmp.dat)[,-1]

So.vlbw <- Surv(time=tmp.dat$time, event=rep(1,nrow(tmp.dat)))
id.vlbw <- seq(nrow(X.vlbw))
cr.vlbw <- NULL

# ##############################################################
# ####### ------- Chandan Reddy DATASETS ----------- ###########

# dir.reddy <- file.path(dir.dataset , 'chandan_reddy')

# # --- (i) worcester_heart_attack --- #
# tmp.dat <- fread(file.path(dir.reddy, 'worcester_heart_attack.csv'))
# So.worcester <- with(tmp.dat, Surv(time=days_in_hospital, event=(died_in_hospital == 'yes')))
# X.worcester <- model.matrix(~age+sex+peak_cardiac+cardiac_shock+first_mycardia,data=tmp.dat)[,-1]
# id.worcester <- tmp.dat$id
# cr.worcester <- NULL

# # --- (ii) vdv --- #
# tmp.dat <- fread(file.path(dir.reddy, 'vdv.csv'))
# So.vdv <- with(tmp.dat, Surv(time=Time, event=(Censoring==1)))
# X.vdv <- as.matrix(tmp.dat[,-(1:2)])
# id.vdv <- seq(nrow(X.vdv))
# cr.vdv <- NULL

# # --- (iii) AML_Bull.csv --- #
# tmp.dat <- fread(file.path(dir.reddy, 'AML_Bull.csv'))
# So.AML <- with(tmp.dat, Surv(time=A1, event=A2))
# X.AML <- as.matrix(tmp.dat[,-(1:3)])
# id.AML <- seq(nrow(X.AML))
# cr.AML <- NULL

# # --- (iv) DBCD.csv --- #
# tmp.dat <- fread(file.path(dir.reddy, 'DBCD.csv'))
# So.DBCD <- with(tmp.dat, Surv(time=A1, event=A2))
# X.DBCD <- as.matrix(tmp.dat[,-(1:3)])
# id.DBCD <- seq(nrow(X.DBCD))
# cr.DBCD <- NULL

# # --- (v) DLBCL --- #
# tmp.dat <- fread(file.path(dir.reddy, 'DLBCL.csv'))
# So.DLBCL <- with(tmp.dat, Surv(time=time, event=status))
# X.DLBCL <- as.matrix(tmp.dat[,-(1:3)])
# id.DLBCL <- seq(nrow(X.DLBCL))
# cr.DLBCL <- NULL

# # --- (vi) NSBCD.csv --- #
# tmp.dat <- fread(file.path(dir.reddy, 'NSBCD.csv'))
# So.NSBCD <- with(tmp.dat, Surv(time=A1, event=A2))
# X.NSBCD <- as.matrix(tmp.dat[,-(1:3)])
# id.NSBCD <- seq(nrow(X.NSBCD))
# cr.NSBCD <- NULL

# ######################################################
# ####### ------- CUSTOMER CHURN ----------- ###########

# dir.churn <- file.path(dir.dataset,'churn')

# # --- (i) Telco Churn --- #
# tmp.dat <- fread(file.path(dir.churn, 'WA_Fn-UseC_-Telco-Customer-Churn.csv'))[as.numeric(order(customerID))]
# # Remove anyone who had tenure==0
# tmp.dat <- tmp.dat[tenure > 0]
# # design + Surv
# So.telco <- with(tmp.dat, Surv(time=tenure, event=(Churn == 'Yes')))
# X.telco <- model.matrix(~.,
#         data=tmp.dat[,which(!colnames(tmp.dat) %in% c('customerID','TotalCharges','Churn','tenure')),with=F])[,-1]
# id.telco <- as.numeric(as.factor(tmp.dat$customerID))
# cr.telco <- NULL
# # Remove perfectly correlated features
# cc.telco <- abs(cor(X.telco))
# X.telco <- X.telco[,!colnames(X.telco) %in% names(unlist(sapply(1:ncol(cc.telco), function(rr) which(cc.telco[rr,][-rr]==1))[c(5,9)]))]

# ################################################################
# ####### ------- OPENML SURVIVAL DATASETS ----------- ###########

# dir.openml <- file.path(dir.dataset, 'openML')


# # https://www.openml.org/d/213
# # --- (ii)  Pharynx --- #
# tmp.dat <- fread(file.path(dir.openml,'dataset_2199_pharynx.csv'))
# # Drop unknown Grade or Conditon
# tmp.dat <- tmp.dat[Grade != '?' & Condition != '?']
# # Aggregated Condition
# tmp.dat[, Condition:= fct_recode(Condition,'01'='0','01'='2','234'='2','234'='3','234'='4') ]

# So.pharynx <- with(tmp.dat, Surv(time = class, event = Status))
# X.pharynx <- model.matrix(~factor(Inst) + factor(sex) + factor(Treatment) + factor(Grade) + Age + 
#                factor(Condition) + factor(Site) + factor(N), data=tmp.dat)[,-1]
# id.pharynx <- seq(nrow(X.pharynx))
# cr.pharynx <- NULL

######################################################
####### ------- OTHER DATASETS ----------- ###########

dir.other <- file.path(dir.dataset, 'other')

# --- (i) AIDS Clinical Trials Group Study 320 Data (actg320.dat) --- #
tmp.dat <- fread(file.path(dir.other, 'actg320.dat'), header=F)
colnames(tmp.dat) <- c('id','time','censor','time_d','censor_d','tx','txgrp','strat2','sex','raceth','ivdrug',
                      'hemophil','karnof','cd4','priorzdv','age')
So.aids320 <- with(tmp.dat, Surv(time=time, event=censor))
tmp.dat[, `:=` (raceth = fct_recode(as.character(raceth),'4+5'='4','4+5'='5'),
               ivdrug = fct_recode(as.character(ivdrug),'2+3'='2','2+3'='3'))]
X.aids320 <- model.matrix(~tx+strat2+factor(sex)+factor(raceth)+factor(ivdrug)+hemophil+karnof+cd4+priorzdv+age,data=tmp.dat)[,-1]
id.aids320 <- as.numeric(as.factor(tmp.dat$id))
cr.aids320 <- NULL

# --- (ii) micro.censure [from plsRcox] --- #

load(file.path(dir.other,'micro.censure.RData'))
tmp.dat <- data.table(micro.censure[,c('survyear','DC','sexe','Agediag','Siege','T','N','M','STADE')])
So.microcensure <- with(tmp.dat, Surv(time=survyear, event=DC))
tmp.dat[, STADE := fct_recode(STADE,'1'='0')]
X.microcensure <- model.matrix(~.,data=tmp.dat[,-(1:2)])[,-1]
id.microcensure <- seq(nrow(X.microcensure))
cr.microcensure <- NULL
# Remove collinear feature
X.microcensure <- X.microcensure[,colnames(X.microcensure) != 'STADE4']

############################################################
####### ------- COMBINE ALL DATASETS ----------- ###########

# Put in list and store
lst.surv <- 
  list(
    ### --- CRAN PACKAGES --- ###
    # survival
    bladder=list(So=So.bladder, X=X.bladder, id=id.bladder, cr=cr.bladder),
    cancer = list(So=So.cancer, X=X.cancer, id=id.cancer, cr=cr.cancer),
    cgd = list(So = So.cgd, X=X.cgd, id=id.cgd, cr=cr.cgd),
    colon = list(So=So.colon, X=X.colon, id=id.colon, cr=cr.colon),
    flchain = list(So = So.flchain, X=X.flchain, id=id.flchain, cr=cr.flchain),
    heart = list(So = So.heart, X=X.heart, id=id.heart, cr=cr.heart), 
    lung = list(So = So.lung, X=X.lung, id=id.lung, cr=cr.lung), 
    mgus = list(So = So.mgus2, X=X.mgus2, id=id.mgus2, cr=cr.mgus2),
    ovarian = list(So=So.ovarian, X=X.ovarian, id=id.ovarian, cr=cr.ovarian),
    pbc = list(So = So.pbc, X=X.pbc, id=id.pbc, cr=cr.pbc), 
    retinopathy = list(So = So.retinopathy, X=X.retinopathy, id=id.retinopathy, cr=cr.retinopathy),
    veteran = list(So = So.veteran, X=X.veteran, id=id.veteran, cr=cr.veteran),
    nwtco = list(So = So.nwtco, X = X.nwtco, id=id.nwtco, cr=cr.nwtco),
    # MASS 
    aids = list(So = So.aids, X=X.aids, id=id.aids, cr=cr.aids),
    melanoma = list(So = So.melanoma, X=X.melanoma, id=id.melanoma, cr=cr.melanoma),
    # coxphf
    breast = list(So = So.breast, X = X.breast, id=id.breast, cr=cr.breast),
    # timereg
    trace = list(So = So.trace, X = X.trace, id=id.trace, cr=cr.trace),
    csl = list(So = So.csl, X = X.csl, id=id.csl, cr=cr.csl),
    bmt = list(So = So.bmt, X = X.bmt, id=id.bmt, cr=cr.bmt),
    diabetes = list(So = So.diabetes, X = X.diabetes, id=id.diabetes, cr=cr.diabetes),
    # eha
    scania = list(So = So.scania, X = X.scania, id=id.scania, cr=cr.scania),
    oldmort = list(So = So.oldmort, X = X.oldmort, id=id.oldmort, cr=cr.oldmort),
    # RobustAFT
    Z243 = list(So = So.Z243, X = X.Z243, id=id.Z243, cr=cr.Z243),
    # AdapEnetClass
    MCL = list(So = So.MCL, X = X.MCL, id=id.MCL, cr=cr.MCL),
    # bujar
    chop = list(So = So.chop, X = X.chop, id=id.chop, cr=cr.chop),
    # survJamda.data
    breast_norway = list(So = So.breast_norway, X = X.breast_norway, id=id.breast_norway, cr=cr.breast_norway),
    breast_duke = list(So = So.breast_duke, X = X.breast_duke, id=id.breast_duke, cr=cr.breast_duke),
    breast_nc = list(So = So.breast_nc, X = X.breast_nc, id=id.breast_nc, cr=cr.breast_nc),
    # CoxRidge 
    ova = list(So = So.ova, X = X.ova, id=id.ova, cr=cr.ova),
    # penalized
    nki70 = list(So = So.nki70, X = X.nki70, id=id.nki70, cr=cr.nki70),
    # rpart
    stagec = list(So = So.stagec, X = X.stagec, id=id.stagec, cr=cr.stagec),
    # TH.data
    wpbc = list(So = So.wpbc, X = X.wpbc, id=id.wpbc, cr=cr.wpbc),
    # randomForestSRC
    follic = list(So = So.follic, X = X.follic, id=id.follic, cr=cr.follic),
    # coin
    glioma = list(So = So.glioma, X = X.glioma, id=id.glioma, cr=cr.glioma), 
    # frailtySurv
    hdfail = list(So = So.hdfail, X = X.hdfail, id=id.hdfail, cr=cr.hdfail), 
    # spBayesSurv
    leukemia = list(So = So.leukemia, X = X.leukemia, id=id.leukemia, cr=cr.leukemia), 
    # NestedCohort
    zinc = list(So = So.zinc, X = X.zinc, id=id.zinc, cr=cr.zinc), 
    # joint.Cox
    ovarian2 = list(So = So.ovarian2, X = X.ovarian2, id=id.ovarian2, cr=cr.ovarian2), 
    # RCASPAR
    bergamaschi = list(So = So.bergamaschi, X = X.bergamaschi, id=id.bergamaschi, cr=cr.bergamaschi), 
    # IPWsurvival
    divat = list(So = So.divat, X = X.divat, id=id.divat, cr=cr.divat),
    # hdnom
    smart = list(So = So.smart, X = X.smart, id=id.smart, cr=cr.smart), 
    # relsurv
    rdata = list(So = So.rdata, X = X.rdata, id=id.rdata, cr=cr.rdata), 
    # pec
    pbc3 = list(So = So.pbc3, X = X.pbc3, id=id.pbc3, cr=cr.pbc3), 
    cost = list(So = So.cost, X = X.cost, id=id.cost, cr=cr.cost), 
    # JM
    aidsJM = list(So = So.aidsJM, X = X.aidsJM, id=id.aidsJM, cr=cr.aidsJM),
    pbc2 = list(So = So.pbc2, X = X.pbc2, id=id.pbc2, cr=cr.pbc2),  
    # asaur
    hepato = list(So = So.hepato, X = X.hepato, id=id.hepato, cr=cr.hepato), 
    smoking = list(So = So.smoking, X = X.smoking, id=id.smoking, cr=cr.smoking), 
    prostate = list(So = So.prostate, X = X.prostate, id=id.prostate, cr=cr.prostate), 
    # RcmdrPlugin.survival
    dialysis = list(So = So.dialysis, X = X.dialysis, id=id.dialysis, cr=cr.dialysis), 
    rossi = list(So = So.rossi, X = X.rossi, id=id.rossi, cr=cr.rossi), 
    # AF
    rotterdam = list(So = So.rotterdam, X = X.rotterdam, id=id.rotterdam, cr=cr.rotterdam), 
    # Ecdat
    unemp1 = list(So = So.unemp1, X = X.unemp1, id=id.unemp1, cr=cr.unemp1),
    unemp2 = list(So = So.unemp2, X = X.unemp2, id=id.unemp2, cr=cr.unemp2),
    # smcure
    ecog = list(So = So.ecog, X = X.ecog, id=id.ecog, cr=cr.ecog), 
    # joineR
    heartvalve = list(So = So.heartvalve, X = X.heartvalve, id=id.heartvalve, cr=cr.heartvalve), 
    epileptic = list(So = So.epileptic, X = X.epileptic, id=id.epileptic, cr=cr.epileptic), 
    # # pckg
    # VV = list(So = So.VV, X = X.VV),  
    ### --- Lifelines datasets --- ###
    anderson = list(So = So.anderson, X=X.anderson, id=id.anderson, cr=cr.anderson),
    divorce = list(So = So.divorce, X=X.divorce, id=id.divorce, cr=cr.divorce),
    kidney = list(So = So.kidney, X=X.kidney, id=id.kidney, cr=cr.kidney),
    larynx  = list(So = So.larynx, X=X.larynx, id=id.larynx, cr=cr.larynx),
    ### --- Vanderbilt datasets --- ###
    support2 = list(So=So.support2, X=X.support2, id=id.support2, cr=cr.support2),
    gbr = list(So = So.gbr, X = X.gbr, id=id.gbr, cr=cr.gbr),
    byar = list(So = So.byar, X = X.byar, id=id.byar, cr=cr.byar),
    framingham = list(So = So.framingham, X = X.framingham, id=id.framingham, cr=cr.framingham),
    RHC = list(So = So.RHC, X = X.RHC, id=id.RHC, cr=cr.RHC),
    catheter = list(So = So.catheter, X = X.catheter, id=id.catheter, cr=cr.catheter),
    ARI = list(So = So.ARI, X = X.ARI, id=id.ARI, cr=cr.ARI),
    vlbw = list(So = So.vlbw, X = X.vlbw, id=id.vlbw, cr=cr.vlbw),
    ### --- Chandan Reddy
    worcester = list(So = So.worcester, X = X.worcester, id=id.worcester, cr=cr.worcester),
    vdv = list(So = So.vdv, X = X.vdv, id=id.vdv, cr=cr.vdv),
    AML = list(So = So.AML, X = X.AML, id=id.AML, cr=cr.AML),
    DBCD = list(So = So.DBCD, X = X.DBCD, id=id.DBCD, cr=cr.DBCD),
    DLBCL = list(So = So.DLBCL, X = X.DLBCL, id=id.DLBCL, cr=cr.DLBCL),
    NSBCD = list(So = So.NSBCD, X = X.NSBCD, id=id.NSBCD, cr=cr.NSBCD),
    employee = list(So = So.employee, X = X.employee, id=id.employee, cr=cr.employee),
    ### --- churn
    telco = list(So = So.telco, X = X.telco, id=id.telco, cr=cr.telco),
    ### --- OPENML
    lungcaner = list(So = So.lungcancer, X = X.lungcancer, id=id.lungcancer, cr=cr.lungcancer),
    pharynx = list(So = So.pharynx, X = X.pharynx, id=id.pharynx, cr=cr.pharynx),
    ### --- Other
    aids320 = list(So = So.aids320, X = X.aids320, id=id.aids320, cr=cr.aids320),
    microcensure = list(So = So.microcensure, X = X.microcensure, id=id.microcensure, cr=cr.microcensure)
  )

# Make sure that none of our time points end on 0...
for (ss in names(lst.surv)) {
  tmp.So <- lst.surv[[ss]]$So
  if( ncol(tmp.So) == 2 ) {
    tmin <- min(tmp.So[,1])
    if (tmin==0) {
      print(sprintf('Dataset %s has event time at 0, adding 1 to all events times',ss))
      tmp.So[,1] <- tmp.So[,1] + 1
      lst.surv[[ss]]$So <- tmp.So
    }
  }
}

# Get dataset features
ds.timedep <- ifelse(unlist(lapply(lst.surv,function(ll) ncol(ll$So) ))==2,F,T)
ds.cens <- mapply(function(ll, td) 1-ifelse(td, mean(ll$So[,3]), mean(ll$So[,2])),lst.surv,ds.timedep)
ds.n <- unlist(lapply(lst.surv,function(ll) nrow(ll$So) ))
ds.n2 <- unlist(lapply(lst.surv,function(ll) nrow(ll$X) ))
ds.n3 <- unlist(lapply(lst.surv,function(ll) length(ll$id) ))
ds.n4 <- lapply(lst.surv,function(ll) nrow(ll$cr) )
ds.n4 <- unlist(lapply(ds.n4, function(ll) ifelse(is.null(ll),0,ll)))
which(ds.n != ds.n3)
which(ds.n[ds.n4!=0] != ds.n4[ds.n4!=0])
ds.p <- unlist(lapply(lst.surv,function(ll) ncol(ll$X) ))
data.table(dataset=names(ds.n),n=ds.n,n2=ds.n2)[n != n2]

# Organize by n
ds.summary <- data.table(dataset=names(lst.surv), n=ds.n, p=ds.p, events=ds.n*(1-ds.cens), cens=round(ds.cens,2), 
                         timedep=ifelse(ds.timedep,'yes','no'), highdim=ifelse(ds.p > ds.n,'yes','no'))[order(-n)]
# Save the list
format(object.size(lst.surv),'MB')
save(lst.surv, file=file.path(dir.output,'surv_datasets.RData'))

# Make a plot
ds.plot <- melt(ds.summary,measure.vars=c('n','p'),variable.name='dimension')
ds.plot[, dimension := fct_recode(dimension, '# of samples'='n','# of features'='p')]

gg.base <- ggplot() + background_grid(major='xy',minor='none') + 
  facet_wrap(~dimension,scales='free') + 
  theme(axis.title = element_blank(), axis.text.x = element_text(angle=90,size=8),
        legend.position = 'bottom',legend.justification = 'center') + 
  scale_color_gradient(low='blue',high='orange', name='Censoring (%): ')
gg1 <- gg.base + geom_point(data=ds.plot[as.numeric(dimension)==1],aes(x=fct_reorder(dataset,value),y=log2(value), color=cens)) + 
  scale_y_continuous(breaks=seq(0,14,2)) 
tmp.leg <- get_legend(gg1)
gg1 <- gg1 + theme(legend.position = 'none')
gg2 <- gg.base + geom_point(data=ds.plot[as.numeric(dimension)==2],aes(x=fct_reorder(dataset,value),y=log2(value), color=cens)) + 
  scale_y_continuous(breaks=seq(0,18,2)) + guides(color=F)
gg.ds.summary <- plot_grid(plot_grid(gg1, gg2, nrow=1, labels = c('n','p')),tmp.leg,rel_heights = c(10,1),ncol=1)
save_plot(filename = file.path(dir.output,'..','figures','gg_surv_desc.png'),plot=gg.ds.summary, base_height=10,base_width = 14)

