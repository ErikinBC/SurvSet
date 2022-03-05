# Process pec datasets
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) Pbc3 --- #
    def process_Pbc3(self, fn = 'Pbc3'):
        path = os.path.join(self.dir_process, '%s.csv' % fn)
        df = pd.read_csv(path,sep=';')
        cn_fac = ['unit','tment','sex','stage','gibleed']
        cn_num = ['age','crea','alb','bili','alkph','asptr','weight']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status'] == 2, 1, 0)  # Death
        # (iii) Feature transform
        di_map = {'unit':{1: 'Hvidovre', 2: 'London', 3: 'Copenhagen', 4: 'Barcelona', 5: 'Munich', 6: 'Lyon'}, 'tment':{0: 'placebo', 1: 'CyA'}, 'sex':{1:'M',0:'F'}, 'gibleed':{1: 'Y', 0: 'N'}}
        self.df_map(df, di_map)
        
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'days', cn_pid='ptno')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) cost --- #
    def process_cost(self, fn = 'cost'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sex','hypTen','ihd','prevStroke','othDisease','alcohol','diabetes','smoke','atrialFib','hemor']
        cn_num = ['age','strokeScore','cholest']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'status', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) GBSG2 --- #
    def process_GBSG2(self, fn = 'GBSG2'):
        path = os.path.join(self.dir_process, '%s.csv' % fn)
        df = pd.read_csv(path,sep=';')
        cn_fac = ['horTh', 'menostat', 'tgrade']
        cn_num = ['age', 'tsize', 'pnodes', 'progrec', 'estrec']
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'cens', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
