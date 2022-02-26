# --- (xxxviii) dataOvarian1 --- #
utils::data(dataOvarian1, package = "joint.Cox")
So.ovarian2 <- with(dataOvarian1, Surv(time=t.event, event=event))
X.ovarian2 <- model.matrix(~.+factor(group),data=dataOvarian1[,-(1:2)])[,-(1:2)]
id.ovarian2 <- seq(nrow(X.ovarian2))
cr.ovarian2 <- NULL
