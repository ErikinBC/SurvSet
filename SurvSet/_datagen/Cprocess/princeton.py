# Process princeton datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline

class package(baseline):
    # --- (i) divorce --- #
    def process_divorce(self, fn = 'divorce'):
        path = os.path.join(self.dir_process, '%s.csv'%fn)
        df = pd.read_csv(path,sep='\\s{2,}',engine='python')
        cn_num = []
        cn_fac = ['heduc', 'heblack', 'mixed']
        # (i) Create event, time, and id
        df['div'] = np.where(df['div'] == 'Yes',1,0)
        # (iii) Feature transform
        df['heduc'] = df['heduc'].str.replace('\\s|years','',regex=True)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'div', 'years')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
