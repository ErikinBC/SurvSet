# Process invGauss datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) d.oropha.rec --- #
    def process_oropha(self, fn = 'd.oropha.rec'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['inst', 'sex', 'treatm', 'grade', 'cond','site', 'tstage', 'nstage']
        cn_num = ['age', 'cond', 'tstage', 'nstage']
        # (iii) Feature transform
        di_map = {'sex':{1:'M',2:'F', 'treatm':{1:'standard',2:'test'}}}
        self.df_map(df, di_map)
        
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
