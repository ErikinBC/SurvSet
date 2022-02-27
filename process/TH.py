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

# --- (xxxii) wpbc --- #
tmp.dat <- TH.data::wpbc
tmp.na.mu <- apply(tmp.dat,2,function(cc) mean(is.na(cc)))
tmp.dat$pnodes <- ifelse(is.na(tmp.dat$pnodes),as.numeric(names(sort(table(tmp.dat$pnodes),decreasing = T)[1])),tmp.dat$pnodes)
So.wpbc <- with(tmp.dat, Surv(time=time, event=(status=='R')))
X.wpbc <- model.matrix(~.,data=tmp.dat[,-(1:2)])[,-1]
id.wpbc <- seq(nrow(X.wpbc))
cr.wpbc <- NULL

