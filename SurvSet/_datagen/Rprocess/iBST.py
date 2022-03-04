# Process iBST datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda, str_subset

class package(baseline):
    # --- (i) burn --- #
    def process_burn(self, fn = 'burn'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'Z1':'treatment', 'Z2':'sex', 'Z3':'race', 'Z4':'burn_area', 'Z5':'burn_head', 'Z6':'burn_buttock', 'Z7':'burn_trunk', 'Z8':'burn_upper_leg', 'Z9':'burn_lower_leg', 'Z10':'burn_resp', 'Z11':'burn_type'}
        self.df_rename(df, di_cn)
        cn_fac = list(np.setdiff1d(list(di_cn.values()),'burn_area'))
        cn_num = ['burn_area']
        # (i) Create event, time, and id
        # (iii) Feature transform
        di_map = {'sex':{0:'M',1:'F'}, 'race':{0:'nonwhite',1:'white'}, 'burn_type':{'1':'chemical', 2:'scald', 3:'eletric', 4:'flame'}, 'treatment':{0:'bath', 1:'cleanse'}}
        di_bool = {k:{1:'Y',0:'N'} for k in np.setdiff1d(str_subset(di_cn.values(), 'burn'),['burn_area','burn_type'])}
        di_map = {**di_map, **di_bool}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'D3', 'T3')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
