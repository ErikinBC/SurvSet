# --- (xxix) ova --- #
utils::data(ova)
So.ova <- with(ova, Surv(time=time, event=death))
X.ova <- model.matrix(~factor(karn)+factor(figo)+diam+factor(diam),data=ova)[,-1]
id.ova <- ova$x
cr.ova <- NULL

