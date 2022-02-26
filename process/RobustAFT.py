
# --- (xxiii) Z243 --- #
utils::data(Z243, package = 'RobustAFT')
tmp.dat <- data.table(Z243)
tmp.dat[, id := as.numeric(as.factor(NoAdm))]
tmp.dat <- tmp.dat[order(id)]
So.Z243 <- with(tmp.dat, Surv(time=LOS, event=Death))
X.Z243 <- model.matrix(~Sex+Age+CouTot+CsansInv+factor(Adm)+BBDaggr+Charls,data=tmp.dat)[,-1]
id.Z243 <- tmp.dat$id
cr.Z243 <- NULL

