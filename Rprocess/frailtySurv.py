# Process frailtySurv datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) hdfail --- #
    def process_hdfail(self, fn = 'hdfail'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['brand', 'type', 'rsc', 'rer', 'psc']
        cn_num = ['temp']
        # (iii) Feature transform
        # Extract model vs version
        u_models = pd.Series(list(df.model.unique()))
        u_brands = u_models.str.split('\\s',1,True)[0]
        u_brands = np.where(u_brands.str.contains('^[ST]'),'ST',u_brands)
        di_brands = dict(zip(u_models, u_brands))
        u_type = u_models.str.split('\\s').apply(lambda x: x[-1],1)
        di_type = dict(zip(u_models, u_type))
        df['brand'] = df['model'].map(di_brands)
        df['type'] = df['model'].map(di_type)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
