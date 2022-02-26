# --- (xlii) Pbc3 --- #
utils::data(Pbc3, package='pec')
tmp.dat <- data.table(Pbc3)
So.pbc3 <- with(tmp.dat, Surv(time=days, event=status==2))
# Median impute 
cn.med <- c('crea','alb','asptr','weight')
tmp.dat[,(cn.med) := lapply(.SD, function(ll) ifelse(is.na(ll),median(ll,na.rm=T),ll)),.SDcols = cn.med]
# X-mat without stage
X.pbc3 <- model.matrix(~factor(unit)+tment+sex+age+gibleed+crea+alb+bili+alkph+asptr+weight,data=tmp.dat)[,-1]
# Run ordinal regression on stage and them predict
library(MASS)
mdl.ord <- polr(factor(tmp.dat$stage) ~ .,data=data.frame(X.pbc3))
tmp.pred <- predict(mdl.ord, newdata=data.frame(X.pbc3))
tmp.dat[, stage := ifelse(is.na(stage),tmp.pred, stage)]
# Merge on stage
X.pbc3 <- cbind(X.pbc3, model.matrix(~factor(stage),data=tmp.dat)[,-1])
id.pbc3 <- seq(nrow(X.pbc3))
cr.pbc3 <- NULL

# --- (xliii) cost --- #
utils::data(cost, package='pec')
So.cost <- with(cost, Surv(time=time, event=status))
X.cost <- model.matrix(~.,data=cost[,-(14:15)])[,-1]
id.cost <- seq(nrow(X.cost))
cr.cost <- NULL

