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
