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
