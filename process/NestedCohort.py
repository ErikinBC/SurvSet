# --- (xxxvii) zinc --- #
utils::data(zinc, package = "NestedCohort")
tmp.dat <- data.table(zinc)[order(as.numeric(as.factor(id8)))]
So.zinc <- with(tmp.dat, Surv(time=futime01, event=ec01))
X.zinc <- model.matrix(~sex+agepill+smoke+drink+basehist+factor(dysp1)+zincset,data=tmp.dat)[,-1]
# Remove perfectly collinear factor
X.zinc <- X.zinc[,colnames(X.zinc) != 'basehistEsophagitis']
id.zinc <- as.numeric(as.factor(tmp.dat$id8))
cr.zinc <- NULL

