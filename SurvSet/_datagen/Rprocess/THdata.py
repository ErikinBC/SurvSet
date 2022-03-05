# Process TH.data datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) wpbc --- #
    def process_wpbc(self, fn = 'wpbc'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = []
        cn_num = list(df.columns[2:])
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 'R', 1, 0)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df


