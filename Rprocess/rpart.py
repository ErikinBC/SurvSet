# Process rpart datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) stagec --- #
    def process_stagec(self, fn = 'stagec'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['ploidy', 'eet', 'grade', 'gleason']
        cn_num = ['age', 'g2', 'gleason']
        # (iii) Feature transform
        di_map = {'eet':{1:'No',2:'Yes'}}
        self.df_map(df, di_map)
        df[cn_fac] = self.fill_fac(df[cn_fac])[cn_fac]
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'pgstat', 'pgtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
