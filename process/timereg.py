# Process X datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) X --- #
    def process_X(self, fn = 'X'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python')
        cn_fac = []
        cn_num = []
        # (i) Create event, time, and id
        # (ii) Subset
        # (iii) Feature transform
        di_map = {}
        self.df_map(df, di_map)
        df[cn_fac] = self.fill_fac(df[cn_fac])
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='', cn_time='')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


cn_surv = ['pid', 'time', 'event']
cn_surv2 = ['pid', 'time', 'time2', 'event']
dir_base = os.getcwd()
dir_output = os.path.join(dir_base, 'output')
dir_pkgs = os.path.join(dir_base, 'pkgs')
self = package(pkg='', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
# self.run_all()

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
