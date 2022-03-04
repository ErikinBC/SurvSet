# Process NestedCohort datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) zinc --- #
    def process_zinc(self, fn = 'zinc'):
        df = load_rda(self.dir_process, '%s.RData' % fn)
        cn_fac = ['sex', 'agestr','dysp1','dysp2', 'smoke', 'drink', 'basehist','sevdysp','moddysp','mildysp','zincset',]        
        cn_num = ['agepill','stdagepill']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='ec01', cn_time='futime01')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df



