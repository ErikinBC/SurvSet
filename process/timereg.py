# Process timereg datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) TRACE --- #
    def process_TRACE(self, fn = 'TRACE'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_bin = ['chf','diabetes','vf']
        cn_fac = ['sex'] + cn_bin
        cn_num = ['wmi','age']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 9, 1, 0)
        # (iii) Feature transform
        di_map = {'sex':{1:'F',0:'M'}}
        di_map = {**di_map,**{k:{1:'present',0:'absent'} for k in cn_bin}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) csl --- #
    def process_csl(self, fn = 'csl'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_fac = ['sex','treat']
        cn_num = ['age','prot','prot.prev','prot.base']
        # (i) Create event, time, and id
        df['visit'] = df.groupby('id').cumcount()+1
        dat_visit = df.groupby('id')[['visit','dc','eventT']].max().reset_index()
        df.drop(columns=['dc','eventT','time'],inplace=True)
        df = dat_visit.merge(df,'right',['id','visit'])
        df['dc'] = df['dc'].fillna(0).astype(int)
        df = df.assign(rt=lambda x: np.where(x['eventT'].notnull(),x['eventT'],x['rt']))
        # (iii) Feature transform
        di_map = {'sex':{0:'F',1:'M'},'treat':{0:'prednisone',1:'placebo'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'dc', 'lt', 'rt', 'id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) diabetes --- #
    def process_diabetes(self, fn = 'diabetes'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path,sep='\\s',engine='python')
        df.columns = df.columns.str.replace('\\"','',regex=True)
        cn_num = ['agedx']
        cn_fac = ['trteye', 'treat', 'adult']
        # df.reset_index(drop=True, inplace=True)
        # (iii) Feature transform
        di_map = {'trteye':{1:'left',2:'right'},'treat':{1:'treated',0:'untreated'},'adult':{1:'<20',2:'>20'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time', cn_pid='id')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # # --- (iv) bmt (simulated data) --- #
    # def process_bmt(self, fn = 'bmt'):
    #     path = os.path.join(self.dir_process, '%s.txt' % fn)
    #     df = pd.read_csv(path,sep='\\s',engine='python')
    #     df.columns = df.columns.str.replace('\\"','',regex=True)
    #     cn_fac = ['platelet', 'tcell']
    #     cn_num = ['age']
    #     # (i) Create event, time, and id
    #     df['event'] = np.where(df['cause'] == 0, 0, 1)  # Death or relapse
    #     # (iv) Define num, fac, and Surv
    #     df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
    #     df = self.add_suffix(df, cn_num, cn_fac)
    #     return fn, df
