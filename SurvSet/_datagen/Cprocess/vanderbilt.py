# Process vanderbilt datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import str_subset

class package(baseline):
    # --- (i) support2 --- #
    def process_support2(self, fn = 'support2'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        dir_support = os.path.join(dir_vanderbilt, '%scsv' % fn)
        path = os.path.join(dir_support, '%s.csv' % fn)
        df = pd.read_csv(path)
        cn_fac = ['sex', 'dzgroup', 'dzclass', 'num.co', 'race', 'diabetes', 'dementia', 'ca', 'dnr', 'sfdm2', 'income']
        cn_num = ['age', 'num.co', 'edu', 'scoma', 'hday', 'sps', 'surv2m', 'surv6m', 'meanbp', 'wblc', 'hrt', 'resp', 'temp', 'pafi', 'alb', 'bili', 'crea', 'sod', 'ph', 'glucose', 'bun', 'urine', 'adlp', 'adls']
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in ['diabetes', 'dementia']}
        self.df_map(df, di_map)
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'd.time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) prostate --- #
    def process_prostate(self, fn = 'prostate'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '%s.xls' % fn)
        df = pd.read_excel(path, engine='xlrd')
        cn_num = ['age', 'wt', 'sbp', 'dbp', 'hg', 'sz', 'sg', 'ap', 'sdate']
        cn_fac = ['stage', 'rx', 'pf', 'hx', 'ekg', 'bm']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 'alive', 0, 1)
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in ['hx', 'bm']}
        self.df_map(df, di_map)
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'dtime')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) Framingham --- #
    def process_Framingham(self, fn = 'Framingham'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '2.20.%s.csv' % fn)
        df = pd.read_csv(path)
        cn_fac = ['sex','month']
        cn_num = ['sbp','dbp','scl','age','bmi']
        # (iii) Feature transform
        di_map = {'sex':{2:'F',1:'M'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'chdfate', 'followup')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iv) rhc --- #
    def process_rhc(self, fn = 'rhc'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '%s.csv' % fn)
        df = pd.read_csv(path).reset_index(drop=True)
        cn_hx = list(str_subset(df.columns, 'hx$'))
        cn_1 = str_subset(df.columns,'1$')
        cn_1_num = list(cn_1[((df[cn_1].dtypes == float) | (df[cn_1].dtypes == int)).values])
        cn_1_fac = list(cn_1[(df[cn_1].dtypes == object).values])
        cn_fac = ['cat1', 'cat2', 'ca', 'sex', 'ninsclas', 'resp', 'card', 'neuro', 'gastr', 'renal', 'meta', 'hema', 'seps', 'trauma', 'ortho', 'race', 'income'] + cn_hx + cn_1_fac
        cn_num = ['age', 'edu', 'adld3p'] + cn_1_num
        # (i) Create event, time, and id
        df = df.assign(death=lambda x: np.where(x['death'] == 'Yes', 1, 0))
        df = df.assign(time=lambda x: np.where(x['death']==1, x['dthdte']-x['sadmdte'], x['lstctdte']-x['sadmdte']).astype(int))
        # (iii) Feature transform
        di_map = {k:{1:'Y',0:'N'} for k in cn_hx}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (v) acath --- #
    def process_acath(self, fn = 'acath'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        path = os.path.join(dir_vanderbilt, '%s.xls' % fn, '%s.xls' % fn)
        df = pd.read_excel(path, engine='xlrd')
        cn_num = ['age', 'choleste']
        cn_fac = ['sex']
        # (iii) Feature transform
        di_map = {'sex':{0:'M', 1:'F'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'sigdz','cad.dur')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (vi) vlbw --- #
    def process_rhc(self, fn = 'vlbw'):
        dir_vanderbilt = os.path.join(self.dir_process, 'vanderbilt')
        fold_vlbw = os.path.join(dir_vanderbilt, 'vlbw')
        path = os.path.join(fold_vlbw, '%s.csv' % fn)
        df = pd.read_csv(path)
        cn_fac = ['race', 'inout', 'delivery', 'pvh', 'ivh', 'ipe', 'sex', 'twn', 'magsulf', 'meth', 'toc', 'vent', 'pneumo', 'pda', 'cld']
        cn_num = ['birth', 'lowph', 'pltct', 'bwt', 'gest', 'lol', 'apg1', ]
        # (ii) Subset
        df = df.query('hospstay > 0').reset_index(drop=True)
        # (iii) Feature transform
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'dead', 'hospstay')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
