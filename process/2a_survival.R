# Process the survival:: datasets

# ------------------ SURVIVAL DATASETS ---------------- #

# (i) bladder
tmp.dat <- data.table(survival::bladder2)
tmp.dat[, number := fct_recode(as.character(number),'2+3'='2','2+3'='3','4+'='4','4+'='5','4+'='6','4+'='8')]
X.bladder <- model.matrix( ~ factor(rx)+factor(number)+size ,data=tmp.dat)[,-1]
So.bladder <- with(survival::bladder2, Surv(start,stop,event))
id.bladder <- as.numeric(as.factor(tmp.dat$id))
cr.bladder <- NULL

# (ii) cancer
So.cancer <- with(survival::cancer, Surv(time, status ==2))
X.cancer <- cancer[,-(2:3)]
idx.na <- apply(X.cancer,2,function(cc) any(is.na(cc)))
X.cancer[,idx.na] <- apply(X.cancer[,idx.na],2,function(cc) ifelse(is.na(cc),median(cc,na.rm=T),cc))
X.cancer$inst <- fct_lump(as.character(X.cancer$inst),prop=0.05)
X.cancer <- model.matrix(~factor(inst) + age + factor(sex) + ph.ecog + ph.karno + meal.cal + wt.loss, data=X.cancer)[,-1]
id.cancer <- seq(nrow(X.cancer))
cr.cancer <- NULL

# (iii) cgd
tmp.dat <- data.table(survival::cgd)
So.cgd <- with(tmp.dat, Surv(tstart,tstop,status==1))
tmp.dat[, center := fct_lump(center,prop=0.05)]
X.cgd <- model.matrix(~factor(center) + treat + sex + age + height + weight + inherit+propylac+hos.cat,data=tmp.dat)[,-1]
# Remove a perfectly collinear factor
X.cgd <- X.cgd[,colnames(X.cgd)!='factor(center)Amsterdam']
id.cgd <- as.numeric(as.factor(tmp.dat$id))
cr.cgd <- NULL

# (iv) colon
tmp.dat <- data.table(survival::colon)
tmp.dat <- tmp.dat[tmp.dat[,.I[etype == max(etype)],by=id]$V1]
# Median/mode fill for NAs
tmp.dat[, `:=` (nodes = ifelse(is.na(nodes),median(nodes,na.rm=T),nodes),
                differ = ifelse(is.na(differ), as.numeric(names(sort(table(differ),decreasing=T)[1])), differ) )]
So.colon <- with(tmp.dat, Surv(time,status))
tmp.dat[, extent:=fct_recode(as.character(extent), '1+2'='1','1+2'='2','3+4'='3','3+4'='4')]
X.colon <- model.matrix(~rx+sex+age+obstruct+adhere+node4+factor(differ)+factor(extent)+surg, data=tmp.dat[,-c(1,2,9,10,15,16)])[,-1]
id.colon <- as.numeric(as.factor(tmp.dat$id))
cr.colon <- NULL

# (v) flchain
tmp.dat <- survival::flchain
So.flchain <- with(tmp.dat, Surv(futime,death))
tmp.dat$creatinine <- ifelse(is.na(tmp.dat$creatinine),median(tmp.dat$creatinine,na.rm = T),tmp.dat$creatinine)
X.flchain <- model.matrix(~age+sex+sample.yr+kappa+lambda+creatinine+mgus,data=tmp.dat)[,-1]
id.flchain <- seq(nrow(X.flchain))
cr.flchain <- NULL

# (vi) heart
So.heart <- with(survival::heart, Surv(start,stop,event))
X.heart <- model.matrix(~age+year+surgery+transplant,data=survival::heart)[,-1]
id.heart <- as.numeric(as.factor(survival::heart$id))
cr.heart <- NULL

# (vii) lung
tmp.dat <- data.table(survival::lung)
tmp.dat[, (colnames(tmp.dat)) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=colnames(tmp.dat) ]
tmp.dat[, `:=` (inst = fct_lump(as.factor(inst),prop=0.05))]
X.lung <- model.matrix(~inst+age+sex+ph.ecog+ph.karno+pat.karno+meal.cal+wt.loss,data=tmp.dat)[,-1]
So.lung <- with(tmp.dat,Surv(time,status==2))
id.lung <- seq(nrow(X.lung))
cr.lung <- NULL

# (viii) mgus2
tmp.dat <- data.table(survival::mgus2)
cn <- c('mspike','hgb','creat')
tmp.dat[, (cn) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=cn ]
So.mgus2 <- with(mgus2, Surv(futime, death))
X.mgus2 <- model.matrix(~age+sex+hgb+creat+mspike+ptime+pstat,data=tmp.dat)[,-1]
id.mgus2 <- as.numeric(as.factor(tmp.dat$id))
cr.mgus2 <- NULL

# (ix) ovarian
So.ovarian <- with(survival::ovarian,Surv(futime,fustat))
X.ovarian <- model.matrix(~age+factor(resid.ds)+factor(rx)+factor(ecog.ps),data=survival::ovarian)[,-1]
id.ovarian <- seq(nrow(X.ovarian))
cr.ovarian <- NULL

# (x) pbc
tmp.dat <- data.table(survival::pbc)
tmp.dat <- tmp.dat[-which(apply(tmp.dat,1,function(rr) sum(is.na(rr)))>2)]
# Fill in the missing values < 5%
cn <- c('copper','platelet')
tmp.dat[, (cn) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)), .SDcols=cn ]
tmp.dat[, edema := fct_recode(as.character(edema),'none'='0','untreated'='0.5','edema'='1')]
X.pbc <- model.matrix(~factor(trt)+age+sex+ascites+hepato+spiders+factor(edema)+bili+
               albumin+copper+alk.phos+ast+platelet+protime+factor(stage),data=tmp.dat)[,-1]
So.pbc <- with(tmp.dat,Surv(time=time,event=(status==2)))
id.pbc <- as.numeric(as.factor(tmp.dat$id))
cr.pbc <- data.table(time=tmp.dat$time, event=tmp.dat$status)

# (xi) retinopathy
So.retinopathy <- with(survival::retinopathy, Surv(futime,status))
X.retinopathy <- model.matrix(~laser+eye+age+type+trt+risk,data=retinopathy)[,-1]
id.retinopathy <- as.numeric(as.factor(survival::retinopathy$id))
cr.retinopathy <- NULL

# (xii) veteran
So.veteran <- with(survival::veteran, Surv(time,status))
X.veteran <- model.matrix(~factor(trt)+celltype+karno+diagtime+age+factor(prior),data=survival::veteran)[,-1]
id.veteran <- seq(nrow(X.veteran))
cr.veteran <- NULL

# (xiii) nwtco
So.nwtco <- with(survival::nwtco, Surv(time=edrel, event=rel))
X.nwtco <- model.matrix(~factor(instit)+factor(histol)+factor(stage)+factor(study)+age+in.subcohort,data=nwtco)[,-1]
id.nwtco <- as.numeric(as.factor(survival::nwtco$seqno))
cr.nwtco <- NULL
