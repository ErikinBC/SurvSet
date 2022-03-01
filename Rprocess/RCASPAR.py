# Process RCASPAR datasets
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) Bergamaschi --- #
    def process_Bergamaschi(self, fn = 'Bergamaschi'):
        # Combination of matrix of data and survival events
        dat = load_rda(self.dir_process, '%s.RData' % fn)
        dat = pd.DataFrame(dat.values, columns=dat.dim_1.values)
        df = load_rda(self.dir_process, 'survData.RData')
        df.reset_index(drop=True, inplace=True)
        cn_fac = []
        cn_num = list(dat.columns)
        cn_surv = ['censored', 'True_STs']
        df = pd.concat(objs=[df[cn_surv],dat],axis=1)
        # (i) Create event, time, and id
        df['event'] = np.where(df['censored'] == 0, 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'True_STs')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
