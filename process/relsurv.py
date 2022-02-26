# --- (xli) rdata --- #
tmp.dat <- relsurv::rdata
So.rdata <- with(tmp.dat, Surv(time=time,event=cens))
X.rdata <- model.matrix(~age+factor(sex)+year,data=tmp.dat)[,-1]
id.rdata <- seq(nrow(X.rdata))
cr.rdata <- NULL
