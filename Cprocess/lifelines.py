# --- (i) Anderson --- #
tmp.dat <- fread(file.path(dir.lifelines, 'anderson.csv'))
So.anderson <- with(tmp.dat, Surv(time=t, event=status))
X.anderson <- model.matrix(~sex+logWBC+Rx,data=tmp.dat)[,-1]
id.anderson <- seq(nrow(X.anderson))
cr.anderson <- NULL

# --- (ii) divorce --- #
tmp.dat <- fread(file.path(dir.lifelines,'divorce.raw'))
colnames(tmp.dat) <- c('id','heduc','heblack','mixed','years','div')
So.divorce <- with(tmp.dat, Surv(time = years, event=div))
X.divorce <- model.matrix(~heduc+heblack+mixed,data=tmp.dat)[,-1]
id.divorce <- as.numeric(as.factor(tmp.dat$id))
cr.divorce <- NULL

# --- (iii) kidney_transplat --- #
tmp.dat <- fread(file.path(dir.lifelines,'kidney_transplant.csv'))
So.kidney <- with(tmp.dat, Surv(time=time,event=death))
X.kidney <- as.matrix(tmp.dat[,-(1:2)])
id.kidney <- seq(nrow(X.kidney))
cr.kidney <- NULL

# --- (iv) larynx --- #
tmp.dat <- fread(file.path(dir.lifelines,'larynx.csv'))
So.larynx <- with(tmp.dat, Surv(time = time, event=death))
X.larynx <- as.matrix(tmp.dat[,-c(1,3)])
id.larynx <- seq(nrow(X.larynx))
cr.larynx <- NULL



