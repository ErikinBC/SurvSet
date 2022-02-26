# --- (xxxiii) wpbc --- #
utils::data(follic, package = "randomForestSRC")
So.follic <- with(follic,Surv(time=time, event=status %in% c(1,2)))
X.follic <- model.matrix(~age+hgb+factor(clinstg)+ch,data=follic)[,-1]
id.follic <- seq(nrow(X.follic))
cr.follic <- data.table(time=follic$time, event=follic$status)

# https://rdrr.io/cran/randomForestSRC/man/vdv.html

