# Process RcmdrPlugin.survival datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda, str_subset

class package(baseline):
    # --- (i) Dialysis --- #
    def process_Dialysis(self, fn = 'Dialysis'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['center', 'disease']
        cn_num = ['age', 'begin']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) Rossi --- #
    def process_Rossi(self, fn = 'Rossi'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        df = df.rename_axis('pid').reset_index()
        cn_fac = ['fin', 'race', 'wexp', 'mar', 'paro', 'prio', 'educ']
        cn_num = ['age']
        cn_emp = list(str_subset(df.columns,'^emp'))
        # (i) Turn into time-dependent format
        dat_mweek = df.groupby('pid')[['week','arrest']].max().reset_index()
        df_long = df.melt('pid',cn_emp,'week','emp')
        df_long = df_long.assign(week=lambda x: x['week'].str.replace('emp','').astype(int))
        df_long = df_long.assign(emp=lambda x: x['emp'].map({'no':0,'yes':1}))
        df_long = df_long.dropna().astype(int).sort_values(['pid','week']).reset_index(drop=True)
        # Keep first row
        df_long = df_long.assign(demp=lambda x: x.groupby('pid')['emp'].diff().fillna(1).astype(int))
        # Substract -1 since intervals are (start, stop]
        df_long = df_long.query('demp != 0').drop(columns='demp').rename(columns={'week':'start'}).assign(start=lambda x: x['start']-1)
        df_long = df_long.assign(stop=lambda x: x.groupby('pid')['start'].shift(-1))
        df_long = df_long.merge(dat_mweek)
        df_long = df_long.assign(stop=lambda x: np.where(x['stop'].isnull(),x['week'],x['stop']).astype(int))
        # Arrest should only occur on last week (if at all)
        df_long = df_long.assign(arrest=lambda x: np.where(x['stop']==x['week'],x['arrest'],0)).drop(columns='week')
        df = df_long.merge(df[['pid']+cn_fac+cn_num],'left','pid')
        # (iv) Define num, fac, and Surv
        cn_fac += ['emp']
        df = self.Surv(df, cn_num, cn_fac, 'arrest', 'start', 'stop', 'pid')
        df = self.add_suffix(df, cn_num, cn_fac)
        df.query('pid == 2').T
        return fn, df
