

###########################################################
####### ------- VANDERBILT DATASETS ----------- ###########

# http://biostat.mc.vanderbilt.edu/wiki/Main/DataSets
# https://biostat.app.vumc.org/wiki/Main/DataSets

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

# # --- (ii) german breast cancer --- #
# tmp <- data.table(read.delim(file.path(dir.vanderbilt, 'gbsg_ba_ca.dat')))
# # matrix and surv
# X.gbr <- model.matrix(~age+meno+size+factor(grade)+nodes+enodes+pgr+er+hormon,data=tmp)[,-1]
# So.gbr <- with(tmp, Surv(time=X_t, event=X_d))
# id.gbr <- as.numeric(as.factor(tmp$id))
# cr.gbr <- NULL

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


