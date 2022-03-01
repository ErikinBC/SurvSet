# Process AF datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) rott2 --- #
    def process_rott2(self, fn = 'rott2'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'size':'tsize', 'pr':'progesterone', 'er':'estrogen'}
        self.df_rename(df, di_cn)
        cn_fac = ['meno', 'tsize', 'grade', 'hormon', 'chemo', 'recent', 'chemo']
        cn_num = ['year', 'age', 'nodes', 'progesterone', 'estrogen']
        # (i) Create event, time, and id
        df['osi'] = np.where(df['osi'] == 'deceased', 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='osi', cn_time='os', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

import os
cn_surv = ['pid', 'time', 'event']
cn_surv2 = ['pid', 'time', 'time2', 'event']
dir_base = os.getcwd()
dir_output = os.path.join(dir_base, 'output')
dir_pkgs = os.path.join(dir_base, 'pkgs')
self = package(pkg='AF', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)
# self.run_all()
