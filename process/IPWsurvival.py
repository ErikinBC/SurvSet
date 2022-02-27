# Process IPWsurvival datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) DIVAT --- #
    def process_DIVAT(self, fn = 'DIVAT'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['hla', 'retransplant', 'ecd']
        cn_num = ['age']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failures', 'times')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

