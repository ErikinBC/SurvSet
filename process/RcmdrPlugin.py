
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
