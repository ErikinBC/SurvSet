# --- (xxxix) Bergamaschi --- #
utils::data(Bergamaschi, package = "RCASPAR")
utils::data(survData, package = "RCASPAR")
tmp.dat <- data.table(survData)
setnames(tmp.dat, old=c('Overall.survival..mons.undivided','Relapse.free.survival..mons.','Status.0.A..1.AWD..2.DOD..3.DOC'),
                  new=c('ost','rfst','tumor_status'))
tmp.dat <- data.table(tmp.dat, Bergamaschi)
tmp.dat[, id := as.numeric(as.factor(ExptID))]
tmp.dat <- tmp.dat[order(id)]
# Create a new censoring indicator for relapse free to boost N_event
tmp.dat[, event_relapse := ifelse(rfst < ost, 1, 0)]
tmp.dat[, event_relapse := ifelse(event_relapse==1,1, ifelse(censored==0,1,0))]
So.bergamaschi <- with(tmp.dat, Surv(time=rfst, event=event_relapse))
tmp.dat[, tumor_status := fct_recode(as.character(tumor_status),'2'='3')]
X.bergamaschi <-  model.matrix(~.,data=tmp.dat[,str_which(colnames(tmp.dat),'IMAGE'),with=F])[,-1]
id.bergamaschi <- as.numeric(as.factor(tmp.dat$ExptID))
cr.bergamaschi <- NULL
