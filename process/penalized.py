# --- (xxx) nki70 --- #
utils::data(nki70)
tmp.dat <- nki70
So.nki70 <- with(tmp.dat, Surv(time,event))
tmp.dat$Grade <- as.character(tmp.dat$Grade)
X.nki70 <- model.matrix(~Diam+N+ER+factor(Grade)+Age,data=tmp.dat[,1:7])[,-1]
X.nki70 <- cbind(X.nki70, as.matrix(tmp.dat[,-(1:7)]))
id.nki70 <- seq(nrow(X.nki70))
cr.nki70 <- NULL
