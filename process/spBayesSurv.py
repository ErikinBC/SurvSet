# --- (xxxvi) LeukSurv --- #
utils::data(LeukSurv, package = "spBayesSurv")
So.leukemia <- with(LeukSurv, Surv(time=time, event=cens) )
LeukSurv$district <- fct_lump(as.character(LeukSurv$district), prop=0.025)
X.leukemia <- model.matrix(~xcoord+ycoord+age+sex+wbc+tpi+factor(district),data=LeukSurv)[,-1]
id.leukemia <- seq(nrow(X.leukemia))
cr.leukemia <- NULL

