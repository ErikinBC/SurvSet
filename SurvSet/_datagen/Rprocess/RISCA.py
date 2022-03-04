# Process the RISCA datasets
import numpy as np
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) DIVAT1 --- #
    def process_DIVAT1(self, fn = 'dataDIVAT1'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        di_cn = {'z':'graft', 'trajectory':'traj'}
        self.df_rename(df, di_cn)
        cn_fac = ['sexR', 'graft', 'year.tx']
        cn_num = ['ageR', 'year.tx']
        # (i) Create event, time, and id
        df = df.assign(failure=lambda x: (~x['traj'].isin([1,12])).astype(int))
        df = df.assign(time=lambda x: np.where(x['traj'].isin([1,12,13,14]), x['time1'], x['time1']+x['time2'] ))
        # (iii) Feature transform
        di_map = {'graft':{0:'No',1:'Yes'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failure', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (ii) DIVAT2 --- #
    def process_DIVAT2(self, fn = 'dataDIVAT2'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['hla', 'retransplant', 'ecd']
        cn_num = ['age']
        # (iii) Feature transform
        di_map = {'hla':{0:'otherwise',1:'high'}, 'retransplant':{0:'first',1:'>1'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'failures', 'times')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (iii) DIVAT3 --- #
    def process_DIVAT3(self, fn = 'dataDIVAT3'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['sexeR','year.tx','ante.diab','pra']
        cn_num = ['ageR','year.tx','ageD']
        # (iii) Feature transform
        self.float2int(df)  # Floats to integers
        di_map = {'sexeR':{1:'M',0:'F'}, 'ante.diab':{1:'Yes',0:'No'}, 'pra':{1:'Detectable',0:'Undetectable'}}
        self.df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'death.time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
