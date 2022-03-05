# Process AF datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) rott2 --- #
    def process_rott2(self, fn = 'rott2'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'size':'tsize', 'pr':'progesterone', 'er':'estrogen'}
        self.df_rename(df, di_cn)
        cn_fac = ['meno', 'tsize', 'grade', 'hormon', 'chemo', 'recent']
        cn_num = ['year', 'age', 'nodes', 'progesterone', 'estrogen']
        # (i) Create event, time, and id
        df['osi'] = np.where(df['osi'] == 'deceased', 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='osi', cn_time='os', cn_pid='pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
