
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
