# Process spBayesSurv datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) LeukSurv --- #
    def process_LeukSurv(self, fn = 'LeukSurv'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','district']
        cn_num = ['xcoord', 'ycoord','age','wbc','tpi']
        # (iii) Feature transform
        di_map = {'sex':{1:'M',0:'F'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
