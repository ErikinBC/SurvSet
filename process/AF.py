# --- (li) rott2 --- #
tmp.dat <- data.table(AF::rott2)[order(pid)]
So.rotterdam <- with(tmp.dat, Surv(time=os, event=(osi=='deceased')))
X.rotterdam <- model.matrix(~year+age+meno+size+meno+size+factor(grade)+nodes+pr+er+hormon+chemo, data=tmp.dat)[,-1]
id.rotterdam <- tmp.dat$pid
cr.rotterdam <- NULL

