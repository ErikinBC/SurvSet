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

# Function to count categorical features
bin.count <- function(df) {
  df <- as.data.frame(df)
  idx.u <- apply(df,2,function(cc) length(unique(cc)))
  idx.leq <- which(idx.u <= 12)
  if (length(idx.leq) > 0) {
    print(apply(df[,idx.leq,drop=F],2,table))
    propv <- apply(df[,which(idx.u <= 12),drop=F],2,function(cc) min(prop.table(table(cc))) )
    if ( any(propv < 0.05) ) {
      print('The following features have a class imbalance < 5%')
      print(propv[propv < 0.05])
    }  
  }
}


##################################################################
####### ------- BUILT IN SURVIVAL DATASETS ----------- ###########



# ------------------ MASS DATASETS ---------------- #

# (xiiv) Aids2: https://rdrr.io/cran/MASS/src/inst/scripts/ch13.R
# This is domain knowledge but the point of this date is thta AZT started being used for AIDS patient in mid-1987 and
#   HIV patient in mid-1990, so the data is usually split
time.depend.covar <- function(data) {
  id <- row.names(data); n <- length(id)
  events <- c(0, 10043, 11139, 12053) # julian days
  crit1 <- matrix(events[1:3], n, 3 ,byrow = TRUE)
  crit2 <- matrix(events[2:4], n, 3, byrow = TRUE)
  diag <- matrix(data$diag,n,3); death <- matrix(data$death,n,3)
  incid <- (diag < crit2) & (death >= crit1); incid <- t(incid)
  indr <- col(incid)[incid]; indc <- row(incid)[incid]
  ind <- cbind(indr, indc); idno <- id[indr]
  state <- data$state[indr]; T.categ <- data$T.categ[indr]
  age <- data$age[indr]; sex <- data$sex[indr]
  late <- indc - 1
  start <- t(pmax(crit1 - diag, 0))[incid]
  stop <- t(pmin(crit2, death + 0.9) - diag)[incid]
  status <- matrix(as.numeric(data$status),n,3)-1 # 0/1
  status[death > crit2] <- 0; status <- status[ind]
  levels(state) <- c("NSW", "Other", "QLD", "VIC")
  levels(T.categ) <- c("hs", "hsid", "id", "het", "haem",
                       "blood", "mother", "other")
  levels(sex) <- c("F", "M")
  data.frame(idno, zid=factor(late), start, stop, status,
             state, T.categ, age, sex)
}
Aids3 <- time.depend.covar(Aids2)
tmp.dat <- data.table(Aids3)
tmp.dat[, `:=` (T.categ = fct_recode(as.character(T.categ),'mother'='other'),
               zid = factor(zid)) ]
X.aids <- model.matrix(~zid+state+sex+T.categ+age,data=tmp.dat)[,-1]
So.aids <- with(tmp.dat, Surv(start,stop,status==1))
id.aids <- as.numeric(as.factor(tmp.dat$idno))
cr.aids <- NULL

# (xv) Melanoma
tmp.dat <- MASS::Melanoma
So.melanoma <- with(tmp.dat, Surv(time, status %in% c(1,3)))
X.melanoma <- model.matrix(~sex+age+year+thickness+ulcer,data=tmp.dat)[,-1]
id.melanoma <- seq(nrow(X.melanoma))
cr.melanoma <- data.table(time=tmp.dat$time, 
                          event=as.numeric(as.character(fct_recode(as.character(tmp.dat$status),'1'='1','0'='2','2'='3'))))

# ------------------ COXPHF DATASETS ---------------- #

# --- (xvi) coxphf::breast --- #
tmp.dat <- coxphf::breast
So.breast <- with(tmp.dat, Surv(time=TIME, event=CENS))
X.breast <- model.matrix(~T+N+G+CD,data=tmp.dat)[,-1]
id.breast <- seq(nrow(X.breast))
cr.breast <- NULL

# ------------------ TIMEREG DATASETS ---------------- #

# --- (xvii) TRACE --- # 
utils::data(TRACE)
tmp.dat <- TRACE
tmp.dat <- tmp.dat[order(as.numeric(as.factor(tmp.dat$id))),]
So.trace <- with(tmp.dat, Surv(time=time, event=(status %in% 7:9)))
X.trace <- model.matrix(~wmi+chf+age+sex+diabetes+vf,data=tmp.dat)[,-1]
id.trace <- as.numeric(as.factor(tmp.dat$id))
cr.trace <- data.table(time=tmp.dat$time,
                       event=as.numeric(as.character(fct_recode(as.character(tmp.dat$status),'1'='9','2'='8','2'='7'))) )

# --- (xviii) csl --- #
utils::data(csl)
tmp.dat <- data.table(csl)
tmp.dat[, idx := seq(.N), by=id]
tmp.dat[, rt2 := ifelse(idx == max(idx), eventT, rt) , by=id]
tmp.dat[, event := ifelse(idx == max(idx),dc,as.integer(0)),by=id]
# Survival
So.csl <- with(tmp.dat, Surv(time=lt, time2=rt2, event=event))
X.csl <- model.matrix(~prot+sex+age+treat+prot.base+prot.prev,data=tmp.dat)[,-1]
id.csl <- as.numeric(as.factor(tmp.dat$id))
cr.csl <- NULL

# --- (xix) bmt --- #
utils::data(bmt,package='timereg')
So.bmt <- with(bmt, Surv(time=time, event=(cause != 0)))
X.bmt <- model.matrix(~platelet+age+tcell,data=bmt)[,-1]
id.bmt <- seq(nrow(X.bmt))
cr.bmt <- data.table(time=bmt$time, event=bmt$cause)

# --- (xx) diabetes --- #
utils::data(diabetes,package = 'timereg')
So.diabetes <- with(diabetes, Surv(time,status))
X.diabetes <- model.matrix(~factor(trteye)+treat+factor(adult)+agedx,data=diabetes)[,-1]
id.diabetes <- as.numeric(as.factor(diabetes$id))
cr.diabetes <- NULL

# ------------------ EHA DATASETS ---------------- #

# --- (xxi) scania --- #
tmp.dat <- eha::scania
So.scania <- with(tmp.dat, Surv(time=exit - enter, event=event))
X.scania <- model.matrix( ~ birthdate + sex + factor(parish) + ses + immigrant ,data=tmp.dat)[,-1]
id.scania <- as.numeric(as.factor(tmp.dat$id))
cr.scania <- NULL

# --- (xxii) oldmort --- #
tmp.dat <- eha::oldmort
So.oldmort <- with(tmp.dat, Surv(time=enter, time2=exit, event=event))
X.oldmort <- model.matrix(~birthdate+sex+civ+ses.50+birthplace+imr.birth+region,data=tmp.dat)[,-1]
id.oldmort <- as.numeric(as.factor(tmp.dat$id))
cr.oldmort <- NULL

# ------------------ RobustAFT DATASETS ---------------- #

# --- (xxiii) Z243 --- #
utils::data(Z243, package = 'RobustAFT')
tmp.dat <- data.table(Z243)
tmp.dat[, id := as.numeric(as.factor(NoAdm))]
tmp.dat <- tmp.dat[order(id)]
So.Z243 <- with(tmp.dat, Surv(time=LOS, event=Death))
X.Z243 <- model.matrix(~Sex+Age+CouTot+CsansInv+factor(Adm)+BBDaggr+Charls,data=tmp.dat)[,-1]
id.Z243 <- tmp.dat$id
cr.Z243 <- NULL

# ------------------ AdapEnetClass DATASETS ---------------- #

# --- (xxiv) MCLcleaned --- #
utils::data(MCLcleaned, package = 'AdapEnetClass')
tmp.dat <- data.table(MCLcleaned)
tmp.dat <- tmp.dat[order(as.numeric(as.factor(ID)))]
So.MCL <- with(tmp.dat, Surv(time=time, event=cens))
X.MCL <- as.matrix(tmp.dat[,-(1:3)])
id.MCL <- as.numeric(as.factor(tmp.dat$ID))
cr.MCL <- NULL

# ------------------ bujar DATASETS ---------------- #

# --- (xxv) chop --- #
utils::data(chop, package = 'bujar')
So.chop <- with(chop, Surv(time=survtime, event=status))
X.chop <- as.matrix(chop[,-(1:2)])
id.chop <- seq(nrow(X.chop))
cr.chop <- NULL

# ------------------ survJamda.data DATASETS ---------------- #

# --- (xxvi) breast_norway [gse4335] --- #
utils::data(gse4335, package = 'survJamda.data')
utils::data(gse4335pheno, package = 'survJamda.data')
# Clinical data
cn.old <- c('Age_at_diagnosis','X._ER_status_.0.neg._1.pos..','T_.tumor_size.',
            'N_.node_status.','M_.metastasis.','Grade','Histology')
cn.new <- c('age','er_status','tumor_size','node_status','metastasis','grade','histology')
X.tmp <- gse4335pheno[,cn.old]
colnames(X.tmp) <- cn.new
# Remove any missing values
idx.keep <- with(X.tmp, which(!(er_status=='na' | tumor_size =='na' | node_status %in% c('na','x') | grade == 'na')))
X.tmp <- X.tmp[idx.keep,]
X.breast_norway.clin <- model.matrix(~age+er_status+tumor_size+node_status+metastasis+grade,data=X.tmp)[,-1]
So.breast_norway <-  with(gse4335pheno[idx.keep,], Surv(time=Overall_survival_.months., event=X.Status_0.A._1.AWD._2.DOD._3.DOC.) )
X.breast_norway <- as.matrix(cbind(X.breast_norway.clin, gse4335[idx.keep,]))
id.breast_norway <- seq(nrow(X.breast_norway))
cr.breast_norway <- NULL

# --- (xxvii) breast_duke [gse4335] --- #
utils::data(gse3143, package = 'survJamda.data')
utils::data(gse3143pheno, package = 'survJamda.data')

So.breast_duke <- with(gse3143pheno, Surv(time=`Survival_Time(months)`,event=`Status(0=alive,1=dead)`))
X.breast_duke <- as.matrix(gse3143)
id.breast_duke <- seq(nrow(X.breast_duke))
cr.breast_duke <- NULL

# --- (xxviii) breast_nc  [gse1992] --- #

utils::data(gse1992)
utils::data(gse1992pheno)

cn.old <- c('Age','ER__.1.positive._0.negative.','Node_status_.1.positive.1_or_more_nodes.._0.negative.',
            'Grade','Size_.1._..2cm._2._.2cm_to_..5cm._3..5cm._4.any_size_with_direct_extension_to_chest_wall_or_skin.',
            'RFS_event_.0.no_relapse.1.relapsed_at_any_site_or_died_of_disease.','RFS_months',
            'Overall_Survival_Event_.0.alive.1.DOD_or_DOC.','Overall_suvival_months')
cn.new <- c('age','er_positive','node_status','grade','size','rfs_event','rfs_months','surv_event','suv_months')
X.tmp <- gse1992pheno[,cn.old]
colnames(X.tmp) <- cn.new
idx.keep <- which(with(X.tmp,!(is.na(er_positive) | is.na(node_status) | is.na(size) | is.na(grade))))
X.tmp <- X.tmp[idx.keep,]
So.breast_nc <- with(X.tmp, Surv(time=rfs_months, event=rfs_event))
X.breast_nc.clin <- model.matrix(~age+factor(er_positive)+factor(node_status)+factor(grade)+factor(size),data=X.tmp)[,-1]
X.breast_nc <- as.matrix(cbind(X.breast_nc.clin, gse1992[idx.keep,]))
id.breast_nc <- seq(nrow(X.breast_nc))
cr.breast_nc <- NULL

# ------------------ CoxRidge DATASETS ---------------- #

# --- (xxix) ova --- #
utils::data(ova)
So.ova <- with(ova, Surv(time=time, event=death))
X.ova <- model.matrix(~factor(karn)+factor(figo)+diam+factor(diam),data=ova)[,-1]
id.ova <- ova$x
cr.ova <- NULL

# ------------------ penalized DATASETS ---------------- #

# --- (xxx) nki70 --- #
utils::data(nki70)
tmp.dat <- nki70
So.nki70 <- with(tmp.dat, Surv(time,event))
tmp.dat$Grade <- as.character(tmp.dat$Grade)
X.nki70 <- model.matrix(~Diam+N+ER+factor(Grade)+Age,data=tmp.dat[,1:7])[,-1]
X.nki70 <- cbind(X.nki70, as.matrix(tmp.dat[,-(1:7)]))
id.nki70 <- seq(nrow(X.nki70))
cr.nki70 <- NULL

# ------------------ rpart DATASETS ---------------- #

# --- (xxxi) stagec --- #
tmp.dat <- data.table(rpart::stagec)
So.stagec <- with(tmp.dat, Surv(time=pgtime, event=pgstat))
# Pad missing values with mode/median
tmp.dat.na.mu <- apply(tmp.dat,2,function(cc) mean(is.na(cc)))
cn.na <- names(which(tmp.dat.na.mu > 0))
idx.na.class <- as.character(sapply(tmp.dat[,cn.na,with=F],class))
cn.na.int <- cn.na[which(idx.na.class == 'integer')]
cn.na.num <- cn.na[which(idx.na.class == 'numeric')]
tmp.dat[, (cn.na.int) := lapply(.SD, function(cc) ifelse(is.na(cc),as.numeric(names(sort(table(cc),decreasing=T)[1])),cc)),
        .SDcols=cn.na.int]
tmp.dat[, (cn.na.num) := lapply(.SD, function(cc) ifelse(is.na(cc),median(cc,na.rm=T),cc)), .SDcols=cn.na.num]
# Aggregate factor
tmp.dat[, `:=` (grade = fct_recode(as.character(grade),'1+2'='1','1+2'='2','3+4'='3','3+4'='4'),
                gleason = fct_recode(as.character(gleason),'3+4+5'='3','3+4+5'='4','3+4+5'='5','8+9+10'='8','8+9+10'='9','8+9+10'='10' ))]
# model matrix
X.stagec <- model.matrix(~pgtime+pgstat+age+factor(eet)+g2+factor(grade)+factor(gleason)+ploidy,data=tmp.dat)[,-1]
id.stagec <- seq(nrow(X.stagec))
cr.stagec <- NULL

# ------------------ TH.data DATASETS ---------------- #

# --- (xxxii) wpbc --- #
tmp.dat <- TH.data::wpbc
tmp.na.mu <- apply(tmp.dat,2,function(cc) mean(is.na(cc)))
tmp.dat$pnodes <- ifelse(is.na(tmp.dat$pnodes),as.numeric(names(sort(table(tmp.dat$pnodes),decreasing = T)[1])),tmp.dat$pnodes)
So.wpbc <- with(tmp.dat, Surv(time=time, event=(status=='R')))
X.wpbc <- model.matrix(~.,data=tmp.dat[,-(1:2)])[,-1]
id.wpbc <- seq(nrow(X.wpbc))
cr.wpbc <- NULL

# ------------------ randomForestSRC DATASETS ---------------- #

# --- (xxxiii) wpbc --- #
utils::data(follic, package = "randomForestSRC")
So.follic <- with(follic,Surv(time=time, event=status %in% c(1,2)))
X.follic <- model.matrix(~age+hgb+factor(clinstg)+ch,data=follic)[,-1]
id.follic <- seq(nrow(X.follic))
cr.follic <- data.table(time=follic$time, event=follic$status)

# ------------------ coin DATASETS ---------------- #

# --- (xxxiv) glioma --- #
So.glioma <- with(coin::glioma, Surv(time=time, event=event))
X.glioma <- model.matrix(~age+sex+histology+group,data=coin::glioma)[,-1]
id.glioma <- seq(nrow(X.glioma))
cr.glioma <- NULL

# ------------------ frailtySurv DATASETS ---------------- #

# --- (xxxv) hdfail --- #
tmp.dat <- data.table(frailtySurv::hdfail)
tmp.dat <- tmp.dat[time <= mean(time)+3*sd(time)]
# Encode model to higher freq
tmp.dat[, model := str_split_fixed(model,pattern='\\s',2)[,1]]
tmp.dat[, model := ifelse(str_detect(model,'^ST'),'ST',model)]
tmp.dat <- tmp.dat[!model %in% c('SAMSUNG','TOSHIBA')]
tmp.dat <- tmp.dat[order(as.numeric(as.factor(serial)))]
So.hdfail <- with(tmp.dat, Surv(time=time, event=status))
X.hdfail <- model.matrix(~temp+rsc+rer+psc+model,data=tmp.dat)[,-1]
id.hdfail <- as.numeric(as.factor(tmp.dat$serial))
cr.hdfail <- NULL

# ------------------ spBayesSurv DATASETS ---------------- #

# --- (xxxvi) LeukSurv --- #
utils::data(LeukSurv, package = "spBayesSurv")
So.leukemia <- with(LeukSurv, Surv(time=time, event=cens) )
LeukSurv$district <- fct_lump(as.character(LeukSurv$district), prop=0.025)
X.leukemia <- model.matrix(~xcoord+ycoord+age+sex+wbc+tpi+factor(district),data=LeukSurv)[,-1]
id.leukemia <- seq(nrow(X.leukemia))
cr.leukemia <- NULL

# ------------------ NestedCohort DATASETS ---------------- #

# --- (xxxvii) zinc --- #
utils::data(zinc, package = "NestedCohort")
tmp.dat <- data.table(zinc)[order(as.numeric(as.factor(id8)))]
So.zinc <- with(tmp.dat, Surv(time=futime01, event=ec01))
X.zinc <- model.matrix(~sex+agepill+smoke+drink+basehist+factor(dysp1)+zincset,data=tmp.dat)[,-1]
# Remove perfectly collinear factor
X.zinc <- X.zinc[,colnames(X.zinc) != 'basehistEsophagitis']
id.zinc <- as.numeric(as.factor(tmp.dat$id8))
cr.zinc <- NULL

# ------------------ joint.Cox DATASETS ---------------- #

# --- (xxxviii) dataOvarian1 --- #
utils::data(dataOvarian1, package = "joint.Cox")
So.ovarian2 <- with(dataOvarian1, Surv(time=t.event, event=event))
X.ovarian2 <- model.matrix(~.+factor(group),data=dataOvarian1[,-(1:2)])[,-(1:2)]
id.ovarian2 <- seq(nrow(X.ovarian2))
cr.ovarian2 <- NULL

# ------------------ RCASPAR DATASETS ---------------- #

# --- (xxxix) Bergamaschi --- #
utils::data(Bergamaschi, package = "RCASPAR")
utils::data(survData, package = "RCASPAR")
tmp.dat <- data.table(survData)
setnames(tmp.dat, old=c('Overall.survival..mons.undivided','Relapse.free.survival..mons.','Status.0.A..1.AWD..2.DOD..3.DOC'),
                  new=c('ost','rfst','tumor_status'))
tmp.dat <- data.table(tmp.dat, Bergamaschi)
tmp.dat[, id := as.numeric(as.factor(ExptID))]
tmp.dat <- tmp.dat[order(id)]
# Create a new censoring indicator for relapse free to boost N_event
tmp.dat[, event_relapse := ifelse(rfst < ost, 1, 0)]
tmp.dat[, event_relapse := ifelse(event_relapse==1,1, ifelse(censored==0,1,0))]
So.bergamaschi <- with(tmp.dat, Surv(time=rfst, event=event_relapse))
tmp.dat[, tumor_status := fct_recode(as.character(tumor_status),'2'='3')]
X.bergamaschi <-  model.matrix(~.,data=tmp.dat[,str_which(colnames(tmp.dat),'IMAGE'),with=F])[,-1]
id.bergamaschi <- as.numeric(as.factor(tmp.dat$ExptID))
cr.bergamaschi <- NULL

# # ------------------ survivALL DATASETS ---------------- #
# 
# # --- (xxxix) nki_subset --- #
# tmp.clin <- Biobase::pData(nki_subset)
# tmp.expr <- t(Biobase::exprs(nki_subset))
# stopifnot(all(rownames(tmp.expr) == tmp.clin$samplename))
# So.nki <- with(tmp.clin, Surv(time=t.dmfs, event=e.dmfs))
# X.nki <- cbind(model.matrix(~age+factor(grade),data=tmp.clin)[,-1],tmp.expr)


# ------------------ IPWsurvival DATASETS ---------------- #

# --- (xl) DIVAT --- #
utils::data(DIVAT, package='IPWsurvival')
So.divat <- with(DIVAT, Surv(time=times, event=failures))
X.divat <- model.matrix(~age+hla+retransplant+ecd,data=DIVAT)[,-1]
id.divat <- seq(nrow(X.divat))
cr.divat <- NULL

# ------------------ hdnom DATASETS ---------------- #

# --- (xl) smart --- #
tmp.dat <- hdnom::smart
colnames(tmp.dat) <- tolower(colnames(tmp.dat))
X.smart <- model.matrix(~factor(sex)+factor(albumin)+factor(smoking)+factor(alcohol),data=tmp.dat)[,-1]
cn.drop <- c('tevent','event','sex','albumin','smoking','alcohol')
X.smart <- cbind(X.smart, as.matrix(tmp.dat[,setdiff(colnames(tmp.dat),cn.drop)]))
So.smart <- with(tmp.dat, Surv(time=tevent, event=event))
id.smart <- seq(nrow(X.smart))
cr.smart <- NULL

# ------------------ relsurv DATASETS ---------------- #

# --- (xli) rdata --- #
tmp.dat <- relsurv::rdata
So.rdata <- with(tmp.dat, Surv(time=time,event=cens))
X.rdata <- model.matrix(~age+factor(sex)+year,data=tmp.dat)[,-1]
id.rdata <- seq(nrow(X.rdata))
cr.rdata <- NULL

# ------------------ pec DATASETS ---------------- #

# --- (xlii) Pbc3 --- #
utils::data(Pbc3, package='pec')
tmp.dat <- data.table(Pbc3)
So.pbc3 <- with(tmp.dat, Surv(time=days, event=status==2))
# Median impute 
cn.med <- c('crea','alb','asptr','weight')
tmp.dat[,(cn.med) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)),.SDcols = cn.med]
# X-mat without stage
X.pbc3 <- model.matrix(~factor(unit)+tment+sex+age+gibleed+crea+alb+bili+alkph+asptr+weight,data=tmp.dat)[,-1]
# Run ordinal regression on stage and them predict
library(MASS)
mdl.ord <- polr(factor(tmp.dat$stage) ~ .,data=data.frame(X.pbc3))
tmp.pred <- predict(mdl.ord, newdata=data.frame(X.pbc3))
tmp.dat[, stage := ifelse(is.na(stage),tmp.pred, stage)]
# Merge on stage
X.pbc3 <- cbind(X.pbc3, model.matrix(~factor(stage),data=tmp.dat)[,-1])
id.pbc3 <- seq(nrow(X.pbc3))
cr.pbc3 <- NULL

# --- (xliii) cost --- #
utils::data(cost, package='pec')
So.cost <- with(cost, Surv(time=time, event=status))
X.cost <- model.matrix(~.,data=cost[,-(14:15)])[,-1]
id.cost <- seq(nrow(X.cost))
cr.cost <- NULL

# ------------------ JM DATASETS ---------------- #

# --- (xliv) aidsJM --- #
tmp.dat <- data.table(JM::aids)
tmp.dat[, id := as.numeric(as.factor(patient))]
tmp.dat <- tmp.dat[order(id)]
So.aidsJM <- with(tmp.dat, Surv(time=start, time2=stop, event=event))
X.aidsJM <- model.matrix(~CD4+drug+gender+prevOI+AZT,data=tmp.dat)[,-1]
id.aidsJM <- tmp.dat$id
cr.aidsJM <- NULL

# --- (xlv) pbc2 --- #
tmp.dat <- data.table(JM::pbc2)
setnames(tmp.dat,c('year','years'),c('start','stop'))
tmp.dat[, id := as.numeric(as.factor(id))]
tmp.dat <- tmp.dat[order(id)]
tmp.dat[, idx := seq(.N), by=id]
tmp.dat[, is_last := ifelse(idx == max(idx),T,F), by=id]
tmp.dat[, status := ifelse(is_last, as.character(status),'alive')]
tmp.dat[, stop2 := shift(start,n=1,type='lead'),by=id]
tmp.dat[, stop2 := ifelse(is_last, stop, stop2) ]
# Surv time
So.pbc2 <- with(tmp.dat, Surv(time=start, time2=stop2, event=(status=='dead')))

# Get the relevant features
cn.vars <- colnames(tmp.dat)[-c(2:3,7,13,20:23)]
tmp.dat2 <- tmp.dat[,cn.vars,with=F]
# Factors to strings
cn.vars.fac <- names(which(sapply(tmp.dat2,class) == 'factor'))
tmp.dat2[, (cn.vars.fac) := lapply(.SD, function(ll) as.character(ll)), .SDcols=cn.vars.fac]
# Loop through each patient and fill with previous value if it's missing
u.ids <- unique(tmp.dat2$id)
lst.store <- vector('list',length(u.ids))
for (ii in seq_along(u.ids)) {
  tmp.id <- u.ids[ii]
  tmp.slice <- tmp.dat2[id == tmp.id]
  counter <- any(is.na(tmp.slice))
  if (counter & any(is.na(tmp.slice[1]))) {
    tmp.slice[1:2, (cn.vars) := lapply(.SD,function(ll) ifelse(is.na(ll), shift(ll,n=1,type='lead'),ll))]
  }
  while ( counter ) {
    tmp.slice[, (cn.vars) := lapply(.SD,function(ll) ifelse(is.na(ll), shift(ll,n=1,type='lag'),ll))]
    counter <- any(is.na(tmp.slice))
  }
  lst.store[[ii]] <- tmp.slice
}
tmp.dat2 <- rbindlist(lst.store)
tmp.dat2[, histologic := as.factor(histologic)]
X.pbc2 <- model.matrix(~.,data=tmp.dat2[,-1])[,-1]
id.pbc2 <- tmp.dat2$id
cr.pbc2 <- data.table(time=tmp.dat$start, time2=tmp.dat$stop2,
             event=as.character(fct_recode(tmp.dat$status,'0'='alive','1'='dead','2'='transplanted')))

# ------------------ asaur DATASETS ---------------- #

# --- (xlvi) hepatoCellular --- #
tmp.dat <- data.table(asaur::hepatoCellular)
tmp.dat <- tmp.dat[,which(apply(tmp.dat,2,function(cc) sum(is.na(cc)))==0),with=F]
So.hepato <- with(tmp.dat, Surv(time=OS, event=Death))
# Make sure binaries are factors
cn.fac <- colnames(tmp.dat)[c(3:15)]
tmp.dat[, (cn.fac) := lapply(.SD, as.factor), .SDcols=cn.fac]
X.hepato <- model.matrix(~.,data=tmp.dat[,-which(colnames(tmp.dat) %in% c('OS','Death','Number','Recurrence')),with=F])[,-1]
id.hepato <- tmp.dat$Number
cr.hepato <- NULL

# --- (xlvii) pharmacoSmoking --- #
tmp.dat <- data.table(asaur::pharmacoSmoking)[order(id)]
tmp.dat[, race := ifelse(race == 'white','white','non-white')]
So.smoking <- with(tmp.dat, Surv(time = ttr, event=relapse))
X.smoking <- model.matrix(~.,data=tmp.dat[,-(1:3)])[,-1]
id.smoking <- tmp.dat$id
cr.smoking <- NULL

# --- (xlviii) prostateSurvival --- #
tmp.dat <- data.table(asaur::prostateSurvival)
So.prostate <- with(tmp.dat, Surv(time=survTime, event=status!=0))
X.prostate <- model.matrix(~grade+stage+ageGroup, data=tmp.dat)[,-1]
id.prostate <- seq(nrow(X.prostate))
cr.prostate <- data.table(time=tmp.dat$survTime, event=tmp.dat$status)

# ------------------ RcmdrPlugin.survival DATASETS ---------------- #

# --- (xlix) Dialysis --- #
load(file.path(dir.dataset,'other','Dialysis.rda'));
tmp.dat <- data.table(Dialysis); rm(Dialysis)
tmp.dat[, center := fct_lump(as.character(center),n=50)]
So.dialysis <- with(tmp.dat, Surv(time=time, event=event))
X.dialysis <- model.matrix(~age+disease+center,data=tmp.dat)[,-1]
id.dialysis <- seq(nrow(X.dialysis))
cr.dialysis <- NULL

# --- (l) Rossi --- #
load(file.path(dir.dataset,'other','Rossi.rda'))
tmp.dat <- data.table(Rossi); rm(Rossi)
# Get the percentage of weeks employed
tmp.pct.emp <- apply(tmp.dat[,-c(1:10)],1,function(rr) sum(na.omit(rr) == 'yes') / length(na.omit(rr)))
tmp.dat <- data.table(tmp.dat[,1:10],pct_emp = tmp.pct.emp)
So.rossi <- with(tmp.dat, Surv(time=week, event=arrest))
X.rossi <- model.matrix(~fin+age+race+wexp+mar+paro+prio+pct_emp+factor(educ),data=tmp.dat)[,-1]
id.rossi <- seq(nrow(X.rossi))
cr.rossi <- NULL

# ------------------ AF DATASETS ---------------- #
# --- (li) rott2 --- #
tmp.dat <- data.table(AF::rott2)[order(pid)]
So.rotterdam <- with(tmp.dat, Surv(time=os, event=(osi=='deceased')))
X.rotterdam <- model.matrix(~year+age+meno+size+meno+size+factor(grade)+nodes+pr+er+hormon+chemo, data=tmp.dat)[,-1]
id.rotterdam <- tmp.dat$pid
cr.rotterdam <- NULL

# ------------------ Ecdat DATASETS ---------------- #

# --- (lii) UnempDur --- #
tmp.dat <- Ecdat::UnempDur
# Remove any patients who are neither jobless nor re-employed
tmp.dat <- tmp.dat[-which(apply(tmp.dat[,2:5],1,sum)==0),]
# Censor1/2/3 are types of re-employment, censor4 is remains jobless
So.unemp1 <- with(tmp.dat, Surv(time=spell, event=(censor4==0)))
X.unemp1 <- model.matrix(~age+ui+reprate+disrate+logwage+tenure,data=tmp.dat)[,-1]
id.unemp1 <- seq(nrow(X.unemp1))
tmp.cr <- as.character(apply(tmp.dat[,2:5],1,function(cc) which(cc == 1)))
tmp.cr <- as.numeric(as.character(fct_recode(tmp.cr,'0'='4')))
cr.unemp1 <- data.table(time=tmp.dat$spell, event=tmp.cr)

# --- (liii) Unemployment --- #
tmp.dat <- Ecdat::Unemployment
So.unemp2 <- with(tmp.dat, Surv(time=duration, event=spell))
# Only use the first survey record data (ftp1) as otherwise features we leak information about duratoin length
X.unemp2 <- model.matrix(~race+sex+reason+search+pubemp+ftp1,data=tmp.dat)[,-1]
id.unemp2 <- seq(nrow(X.unemp2))
cr.unemp2 <- NULL

# ------------------ smcure DATASETS ---------------- #

# --- (liv) Eastern Cooperative Oncology Group (ECOG) data --- #
utils::data(e1684, package='smcure')
tmp.dat <- e1684
# one row is missing age/sex, but receiving treatment so assign to conditional average
tmp.age <- with(tmp.dat,tapply(AGE, TRT, mean,na.rm=T))['1']
tmp.sex <- as.numeric(names(which.max(with(tmp.dat,table(SEX,TRT))[,'1'])))
idx.missing <- which(apply(tmp.dat,1,function(rr) any(is.na(rr))))
tmp.dat[idx.missing,'AGE'] <- tmp.age
tmp.dat[idx.missing,'SEX'] <- tmp.sex
So.ecog <- with(tmp.dat, Surv(time=FAILTIME, event=FAILCENS))
X.ecog <- model.matrix(~TRT+AGE+SEX,data=tmp.dat)[,-1]
colnames(X.ecog) <- tolower(colnames(X.ecog))
id.ecog <- seq(nrow(X.ecog))
cr.ecog <- NULL

# ------------------ joineR DATASETS ---------------- #

# --- (lv) heart.valve --- #
tmp.dat <- data.table(joineR::heart.valve)

# Time-dependent survival object
tmp.dat2 <- tmp.dat[,c('num','time','fuyrs','status')]
tmp.dat2[, `:=` (idx=seq(.N), time.lag1=shift(time,1,type='lag'), time.lead1=shift(time,1,type='lead')),by=num]
tmp.dat2[, `:=` (tstart=ifelse(idx==1,0,time.lag1),tstop=ifelse(idx==max(idx),fuyrs,time)), by=num]
# For the few samples with baseline observations
tmp.dat2[num %in% tmp.dat2[time==0]$num, `:=` (tstop=time.lead1, tstart=time), by=num]
# Then drop any rows with tstop NA
idx.drop <- which(is.na(tmp.dat2$tstop))
tmp.dat2 <- tmp.dat2[-idx.drop,]
So.heartvalve <- with(tmp.dat2, Surv(time=tstart, time2=tstop, event=status))

# Change high colestoral
tmp.dat[, `:=` (hc = fct_recode(as.character(hc),'absent'='0','present'='1','present'='2'),
                emergenc = fct_recode(as.character(emergenc),'elective'='0','urgent'='1','urgent'='2'))]

# design matrix
X.heartvalve <- model.matrix(~sex+age+lvmi+log.lvmi+ef+bsa+lvh+prenyha+redo+size+con.cabg+creat+dm+acei+
                               lv+emergenc+hc+sten.reg.mix+hs,data=tmp.dat)[,-1]
X.heartvalve <- X.heartvalve[-idx.drop,]
id.heartvalve <- tmp.dat$num[-idx.drop]
cr.heartvalve <- NULL

# --- (lvi) epileptic --- #
tmp.dat <- data.table(joineR::epileptic)
tmp.dat <- tmp.dat[time != with.time]
tmp.dat[, `:=` (idx=seq(.N), time.lag=shift(time,1,type='lag')), by=id]
tmp.dat[, `:=` (tstart=ifelse(idx==1,0,time.lag),
                tstop=ifelse(idx==max(idx),with.time,time),
                event=as.integer(0)), by=id ]
tmp.dat[, event := ifelse(idx==max(idx),with.status,event), by=id]
So.epileptic <- with(tmp.dat,Surv(time=tstart,time2=tstop,event=event) )
X.epileptic <- model.matrix(~dose+treat+age+gender+learn.dis,data=tmp.dat)[,-1]
id.epileptic <- tmp.dat$id
cr.epileptic <- NULL


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

##############################################################
####### ------- Chandan Reddy DATASETS ----------- ###########

dir.reddy <- file.path(dir.dataset , 'chandan_reddy')

# --- (i) worcester_heart_attack --- #
tmp.dat <- fread(file.path(dir.reddy, 'worcester_heart_attack.csv'))
So.worcester <- with(tmp.dat, Surv(time=days_in_hospital, event=(died_in_hospital == 'yes')))
X.worcester <- model.matrix(~age+sex+peak_cardiac+cardiac_shock+first_mycardia,data=tmp.dat)[,-1]
id.worcester <- tmp.dat$id
cr.worcester <- NULL

# --- (ii) vdv --- #
tmp.dat <- fread(file.path(dir.reddy, 'vdv.csv'))
So.vdv <- with(tmp.dat, Surv(time=Time, event=(Censoring==1)))
X.vdv <- as.matrix(tmp.dat[,-(1:2)])
id.vdv <- seq(nrow(X.vdv))
cr.vdv <- NULL

# --- (iii) AML_Bull.csv --- #
tmp.dat <- fread(file.path(dir.reddy, 'AML_Bull.csv'))
So.AML <- with(tmp.dat, Surv(time=A1, event=A2))
X.AML <- as.matrix(tmp.dat[,-(1:3)])
id.AML <- seq(nrow(X.AML))
cr.AML <- NULL

# --- (iv) DBCD.csv --- #
tmp.dat <- fread(file.path(dir.reddy, 'DBCD.csv'))
So.DBCD <- with(tmp.dat, Surv(time=A1, event=A2))
X.DBCD <- as.matrix(tmp.dat[,-(1:3)])
id.DBCD <- seq(nrow(X.DBCD))
cr.DBCD <- NULL

# --- (v) DLBCL --- #
tmp.dat <- fread(file.path(dir.reddy, 'DLBCL.csv'))
So.DLBCL <- with(tmp.dat, Surv(time=time, event=status))
X.DLBCL <- as.matrix(tmp.dat[,-(1:3)])
id.DLBCL <- seq(nrow(X.DLBCL))
cr.DLBCL <- NULL

# --- (vi) NSBCD.csv --- #
tmp.dat <- fread(file.path(dir.reddy, 'NSBCD.csv'))
So.NSBCD <- with(tmp.dat, Surv(time=A1, event=A2))
X.NSBCD <- as.matrix(tmp.dat[,-(1:3)])
id.NSBCD <- seq(nrow(X.NSBCD))
cr.NSBCD <- NULL

# --- (vii) employee_attrition.csv --- #
tmp.dat <- fread(file.path(dir.reddy, 'employee_attrition.csv'))
tmp.dat[, BusinessTravel := factor(BusinessTravel, levels=c('Travel_Rarely','Travel_Frequently','Non-Travel'))]
So.employee <- with(tmp.dat, Surv(time=YearsAtCompany,Attrition=='Yes') )

X.employee <- model.matrix(~Age + BusinessTravel + DailyRate + Department + DistanceFromHome + 
               Education + EducationField + EnvironmentSatisfaction + Gender + HourlyRate + 
               JobInvolvement + JobLevel + JobRole + JobSatisfaction + MaritalStatus + 
               MonthlyIncome + MonthlyRate + NumCompaniesWorked + OverTime + PercentSalaryHike + 
               PerformanceRating + RelationshipSatisfaction + StockOptionLevel + TrainingTimesLastYear, data=tmp.dat)[,-1]
id.employee <- seq(nrow(X.employee))
cr.employee <- NULL

######################################################
####### ------- CUSTOMER CHURN ----------- ###########

dir.churn <- file.path(dir.dataset,'churn')

# --- (i) Telco Churn --- #
tmp.dat <- fread(file.path(dir.churn, 'WA_Fn-UseC_-Telco-Customer-Churn.csv'))[as.numeric(order(customerID))]
# Remove anyone who had tenure==0
tmp.dat <- tmp.dat[tenure > 0]
# design + Surv
So.telco <- with(tmp.dat, Surv(time=tenure, event=(Churn == 'Yes')))
X.telco <- model.matrix(~.,
        data=tmp.dat[,which(!colnames(tmp.dat) %in% c('customerID','TotalCharges','Churn','tenure')),with=F])[,-1]
id.telco <- as.numeric(as.factor(tmp.dat$customerID))
cr.telco <- NULL
# Remove perfectly correlated features
cc.telco <- abs(cor(X.telco))
X.telco <- X.telco[,!colnames(X.telco) %in% names(unlist(sapply(1:ncol(cc.telco), function(rr) which(cc.telco[rr,][-rr]==1))[c(5,9)]))]

################################################################
####### ------- OPENML SURVIVAL DATASETS ----------- ###########

dir.openml <- file.path(dir.dataset, 'openML')

# https://www.openml.org/d/1245
# --- (i) lungcancer - Shedden [phpl04K8a] --- #
tmp.dat <- fread(file.path(dir.openml,'phpl04K8a.csv'))
cn.clean <- c('OS_event','histology','sex')
tmp.dat[, (cn.clean) := lapply(.SD, function(ll) str_remove_all(ll,"\\'")), .SDcols=cn.clean]
tmp.dat[, `:=` (OS_years = round(OS_years, 3), OS_event=as.numeric(OS_event))]
X.lungcancer <- model.matrix(~., data=tmp.dat[,-(1:3)])[,-1]
So.lungcancer <- with(tmp.dat, Surv(time=OS_years, event=OS_event))
id.lungcancer <- seq(nrow(X.lungcancer))
cr.lungcancer <- NULL

# https://www.openml.org/d/213
# --- (ii)  Pharynx --- #
tmp.dat <- fread(file.path(dir.openml,'dataset_2199_pharynx.csv'))
# Drop unknown Grade or Conditon
tmp.dat <- tmp.dat[Grade != '?' & Condition != '?']
# Aggregated Condition
tmp.dat[, Condition:= fct_recode(Condition,'01'='0','01'='2','234'='2','234'='3','234'='4') ]

So.pharynx <- with(tmp.dat, Surv(time = class, event = Status))
X.pharynx <- model.matrix(~factor(Inst) + factor(sex) + factor(Treatment) + factor(Grade) + Age + 
               factor(Condition) + factor(Site) + factor(N), data=tmp.dat)[,-1]
id.pharynx <- seq(nrow(X.pharynx))
cr.pharynx <- NULL

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

