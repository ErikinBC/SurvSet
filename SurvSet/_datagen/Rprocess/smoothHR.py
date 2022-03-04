# Process smoothHR datasets
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) whas500 --- #
    def process_whas500(self, fn = 'whas500'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['gender', 'cvd','afb','sho','chf','av3','miord','mitype','year']
        cn_num = ['age', 'hr', 'sysbp', 'diasbp', 'bmi','los','week']
        # (ii) Subset
        # Remove patients who died in the hospital (since we are using LOS as a feature)
        df = df.query('dstat == 0')
        # (iii) Feature transform
        di_map = {'gender':{0:'M',1:'F'}, 'year':{1:'1996-7',2:'1998-9',3:'2001'}}
        self.df_map(df, di_map)
        df = df.assign(admitdate = lambda x: pd.to_datetime(x['admitdate'],format='%d-%m-%Y'))
        df = df.assign(week = lambda x: x['admitdate'].dt.isocalendar()['week'])
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'fstat', 'lenfol')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
