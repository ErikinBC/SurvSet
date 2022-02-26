# --- (xxi) scania --- #
tmp.dat <- eha::scania
So.scania <- with(tmp.dat, Surv(time=exit - enter, event=event))
X.scania <- model.matrix( ~ birthdate + sex + factor(parish) + ses + immigrant ,data=tmp.dat)[,-1]
id.scania <- as.numeric(as.factor(tmp.dat$id))
cr.scania <- NULL

# --- (xxii) oldmort --- #
tmp.dat <- eha::oldmort
So.oldmort <- with(tmp.dat, Surv(time=enter, time2=exit, event=event))
X.oldmort <- model.matrix(~birthdate+sex+civ+ses.50+birthplace+imr.birth+region,data=tmp.dat)[,-1]
id.oldmort <- as.numeric(as.factor(tmp.dat$id))
cr.oldmort <- NULL

