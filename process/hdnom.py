# --- (xl) smart --- #
tmp.dat <- hdnom::smart
colnames(tmp.dat) <- tolower(colnames(tmp.dat))
X.smart <- model.matrix(~factor(sex)+factor(albumin)+factor(smoking)+factor(alcohol),data=tmp.dat)[,-1]
cn.drop <- c('tevent','event','sex','albumin','smoking','alcohol')
X.smart <- cbind(X.smart, as.matrix(tmp.dat[,setdiff(colnames(tmp.dat),cn.drop)]))
So.smart <- with(tmp.dat, Surv(time=tevent, event=event))
id.smart <- seq(nrow(X.smart))
cr.smart <- NULL

