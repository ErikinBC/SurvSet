
# # https://www.openml.org/d/1245
# # --- (i) lungcancer - Shedden [phpl04K8a] --- #
# tmp.dat <- fread(file.path(dir.openml,'phpl04K8a.csv'))
# cn.clean <- c('OS_event','histology','sex')
# tmp.dat[, (cn.clean) := lapply(.SD, function(ll) str_remove_all(ll,"\\'")), .SDcols=cn.clean]
# tmp.dat[, `:=` (OS_years = round(OS_years, 3), OS_event=as.numeric(OS_event))]
# X.lungcancer <- model.matrix(~., data=tmp.dat[,-(1:3)])[,-1]
# So.lungcancer <- with(tmp.dat, Surv(time=OS_years, event=OS_event))
# id.lungcancer <- seq(nrow(X.lungcancer))
# cr.lungcancer <- NULL