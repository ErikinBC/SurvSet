
# --- (lv) heart.valve --- #
tmp.dat <- data.table(joineR::heart.valve)

# Time-dependent survival object
tmp.dat2 <- tmp.dat[,c('num','time','fuyrs','status')]
tmp.dat2[, `:=` (idx=seq(.N), time.lag1=shift(time,1,type='lag'), time.lead1=shift(time,1,type='lead')),by=num]
tmp.dat2[, `:=` (tstart=ifelse(idx==1,0,time.lag1),tstop=ifelse(idx==max(idx),fuyrs,time)), by=num]
# For the few samples with baseline observations
tmp.dat2[num %in% tmp.dat2[time==0]$num, `:=` (tstop=time.lead1, tstart=time), by=num]
# Then drop any rows with tstop NA
idx.drop <- which(is.na(tmp.dat2$tstop))
tmp.dat2 <- tmp.dat2[-idx.drop,]
So.heartvalve <- with(tmp.dat2, Surv(time=tstart, time2=tstop, event=status))

# Change high colestoral
tmp.dat[, `:=` (hc = fct_recode(as.character(hc),'absent'='0','present'='1','present'='2'),
                emergenc = fct_recode(as.character(emergenc),'elective'='0','urgent'='1','urgent'='2'))]

# design matrix
X.heartvalve <- model.matrix(~sex+age+lvmi+log.lvmi+ef+bsa+lvh+prenyha+redo+size+con.cabg+creat+dm+acei+
                               lv+emergenc+hc+sten.reg.mix+hs,data=tmp.dat)[,-1]
X.heartvalve <- X.heartvalve[-idx.drop,]
id.heartvalve <- tmp.dat$num[-idx.drop]
cr.heartvalve <- NULL

# --- (lvi) epileptic --- #
tmp.dat <- data.table(joineR::epileptic)
tmp.dat <- tmp.dat[time != with.time]
tmp.dat[, `:=` (idx=seq(.N), time.lag=shift(time,1,type='lag')), by=id]
tmp.dat[, `:=` (tstart=ifelse(idx==1,0,time.lag),
                tstop=ifelse(idx==max(idx),with.time,time),
                event=as.integer(0)), by=id ]
tmp.dat[, event := ifelse(idx==max(idx),with.status,event), by=id]
So.epileptic <- with(tmp.dat,Surv(time=tstart,time2=tstop,event=event) )
X.epileptic <- model.matrix(~dose+treat+age+gender+learn.dis,data=tmp.dat)[,-1]
id.epileptic <- tmp.dat$id
cr.epileptic <- NULL
