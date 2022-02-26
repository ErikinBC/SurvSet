# Process AdapEnetClass datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda, str_subset

class package(baseline):
    # --- (i) X --- #
    def process_X(self, fn = 'MCLcleaned'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = []
        cn_num = list(str_subset(df.columns,'^X'))
        # (i) Create event, time, and id
        # (ii) Subset
        # (iii) Feature transform
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time', cn_pid='ID')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
