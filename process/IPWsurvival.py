# --- (xl) DIVAT --- #
utils::data(DIVAT, package='IPWsurvival')
So.divat <- with(DIVAT, Surv(time=times, event=failures))
X.divat <- model.matrix(~age+hla+retransplant+ecd,data=DIVAT)[,-1]
id.divat <- seq(nrow(X.divat))
cr.divat <- NULL

