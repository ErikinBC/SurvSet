# Process bujar datasets
import os
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) chop --- #
    def process_chop(self, fn = 'chop'):
        # Merge chop and rchop datasets
        df1 = load_rda(self.dir_process, '%s.rda' % fn)
        df2 = load_rda(self.dir_process, 'r%s.rda' % fn)
        df = pd.concat(objs=[df1, df2], axis=0)
        df.reset_index(drop=True, inplace=True)
        del df1, df2
        cn_fac = []
        cn_num = list(df.columns[2:])        
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'survtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
