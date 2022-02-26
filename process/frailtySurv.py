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
