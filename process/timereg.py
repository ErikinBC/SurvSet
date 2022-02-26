
# --- (xvii) TRACE --- # 
utils::data(TRACE)
tmp.dat <- TRACE
tmp.dat <- tmp.dat[order(as.numeric(as.factor(tmp.dat$id))),]
So.trace <- with(tmp.dat, Surv(time=time, event=(status %in% 7:9)))
X.trace <- model.matrix(~wmi+chf+age+sex+diabetes+vf,data=tmp.dat)[,-1]
id.trace <- as.numeric(as.factor(tmp.dat$id))
cr.trace <- data.table(time=tmp.dat$time,
                       event=as.numeric(as.character(fct_recode(as.character(tmp.dat$status),'1'='9','2'='8','2'='7'))) )

# --- (xviii) csl --- #
utils::data(csl)
tmp.dat <- data.table(csl)
tmp.dat[, idx := seq(.N), by=id]
tmp.dat[, rt2 := ifelse(idx == max(idx), eventT, rt) , by=id]
tmp.dat[, event := ifelse(idx == max(idx),dc,as.integer(0)),by=id]
# Survival
So.csl <- with(tmp.dat, Surv(time=lt, time2=rt2, event=event))
X.csl <- model.matrix(~prot+sex+age+treat+prot.base+prot.prev,data=tmp.dat)[,-1]
id.csl <- as.numeric(as.factor(tmp.dat$id))
cr.csl <- NULL

# --- (xix) bmt --- #
utils::data(bmt,package='timereg')
So.bmt <- with(bmt, Surv(time=time, event=(cause != 0)))
X.bmt <- model.matrix(~platelet+age+tcell,data=bmt)[,-1]
id.bmt <- seq(nrow(X.bmt))
cr.bmt <- data.table(time=bmt$time, event=bmt$cause)

# --- (xx) diabetes --- #
utils::data(diabetes,package = 'timereg')
So.diabetes <- with(diabetes, Surv(time,status))
X.diabetes <- model.matrix(~factor(trteye)+treat+factor(adult)+agedx,data=diabetes)[,-1]
id.diabetes <- as.numeric(as.factor(diabetes$id))
cr.diabetes <- NULL
