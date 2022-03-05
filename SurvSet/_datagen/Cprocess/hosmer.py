# Process hosmer datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline

class package(baseline):
    # --- (i) uis --- #
    def process_uis(self, fn = 'uis'):
        dir_hosmer = os.path.join(self.dir_process, 'hosmer')
        path = os.path.join(dir_hosmer, '%s.csv' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python', header=None)
        df = df.replace('.',np.nan)
        cn = ['id', 'age', 'beck', 'heroic', 'ivhx', 'ndrugtx', 'race', 'treat', 'site', 'los', 'time', 'censor']
        df.columns = cn
        cn_fac = ['heroic', 'ivhx', 'race', 'treat', 'site']
        cn_num = ['age', 'beck', 'ndrugtx']
        # (iii) Feature transform
        di_map = {'heroic':{'1':'Heroin&Cocaine','2':'Heroin','3':'Cocaine','4':'Neither',np.nan:np.nan}, 'ivhx':{'1':'Never','2':'Previous','3':'Recent', np.nan:np.nan}, 'race':{'0':'white','1':'other',np.nan:np.nan}, 'treat':{0:'short', 1:'long'}, 'site':{0:'A',1:'B'}}
        self.df_map(df, di_map)
        
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'censor', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) FRTCS --- #
    def process_FRTCS(self, fn = 'FRTCS'):
        dir_hosmer = os.path.join(self.dir_process, 'hosmer')
        path = os.path.join(dir_hosmer, '%s.csv' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python', header=None)
        df = df.replace('.',np.nan)
        cn = ['id', 'age', 'sex', 'date0', 'spb0', 'dbp0', 'antihyp0', 'date1', 'spb1', 'dpb1', 'antihyp1', 'date2', 'spb2', 'dpb2', 'antihyp2', 'date_event', 'censor']
        df.columns = cn
        cn_fac = ['sex', 'antihyp0', 'antihyp1', 'antihyp2']
        cn_num = ['age', 'spb0', 'dbp0', 'spb1', 'dpb1', 'spb2', 'dpb2', 'date0', 'date1']
        # (iii) Feature transform
        cn_date = ['date_event', 'date0', 'date1', 'date2']
        df[cn_date] = df[cn_date].apply(lambda x: pd.to_datetime(x, format='%d%b%y'))
        df_date = df.melt(['id','date2'],cn_date[:-1],'msr','date')
        df_date = df_date.assign(days=lambda x: ((x['date2']-x['date']).dt.total_seconds() / (60*60*24)).astype(int))
        df_date = df_date.assign(days=lambda x: np.where(x['msr']=='date_event', -x['days'], x['days']))
        df_date = df_date.pivot('id','msr','days').reset_index()
        df = df.drop(columns=cn_date).merge(df_date)
        # Drug treatments
        di_map = {**{'sex':{1:'M',2:'F'}}, **{k:{1:'Y',0:'N'} for k in cn_fac[1:]}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'censor', 'date_event')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
