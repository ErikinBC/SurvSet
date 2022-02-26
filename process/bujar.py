# --- (xxv) chop --- #
utils::data(chop, package = 'bujar')
So.chop <- with(chop, Surv(time=survtime, event=status))
X.chop <- as.matrix(chop[,-(1:2)])
id.chop <- seq(nrow(X.chop))
cr.chop <- NULL
