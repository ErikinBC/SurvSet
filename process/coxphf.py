# Process coxphf datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline

class package(baseline):
    # --- (i) breast --- #
    def process_breast(self, fn = 'breast'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python')
        cn_fac = ['T','N','G','CD']
        cn_num = []
        df = df.drop_duplicates()
        # (iii) Feature transform
        di_map = {k:{1:'Unfavourable', 0:'Favourable'} for k in cn_fac}
        self.df_map(df, di_map)
        # (iv) Define Surv, and rename
        df = self.Surv(df, cn_num, cn_fac, 'CENS', 'TIME')
        df = self.add_suffix(df, cn_num, cn_fac)
        di_cn = {'T':'TumorStage', 'N':'NodalStatus', 'G':'Histology','CD':'CathepsinD'}
        di_cn = {'fac_'+k:'fac_'+v for k,v in di_cn.items()}
        self.df_rename(df, di_cn)
        return fn, df




# import os
# cn_surv = ['pid', 'time', 'event']
# cn_surv2 = ['pid', 'time', 'time2', 'event']
# dir_base = os.getcwd()
# dir_output = os.path.join(dir_base, 'output')
# dir_pkgs = os.path.join(dir_base, 'pkgs')
# self = package(pkg='coxphf', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
# self.run_all()

# (i) Create event, time, and id
# (ii) Subset
# (iii) Feature transform
# (iv) Define num, fac, and Surv

# # --- (xvi) coxphf::breast --- #
# tmp.dat <- coxphf::breast
# So.breast <- with(tmp.dat, Surv(time=TIME, event=CENS))
# X.breast <- model.matrix(~T+N+G+CD,data=tmp.dat)[,-1]
# id.breast <- seq(nrow(X.breast))
# cr.breast <- NULL