# --- (xxxii) wpbc --- #
tmp.dat <- TH.data::wpbc
tmp.na.mu <- apply(tmp.dat,2,function(cc) mean(is.na(cc)))
tmp.dat$pnodes <- ifelse(is.na(tmp.dat$pnodes),as.numeric(names(sort(table(tmp.dat$pnodes),decreasing = T)[1])),tmp.dat$pnodes)
So.wpbc <- with(tmp.dat, Surv(time=time, event=(status=='R')))
X.wpbc <- model.matrix(~.,data=tmp.dat[,-(1:2)])[,-1]
id.wpbc <- seq(nrow(X.wpbc))
cr.wpbc <- NULL

