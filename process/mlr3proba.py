# Process for mlr3proba
from funs_class import baseline
from funs_support import load_rda

class package(baseline):
    # --- (i) grace --- #
    def process_grace(self, fn = 'grace'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['revasc', 'stchange']
        cn_num = ['los', 'age', 'sysbp']
        # (iii) Feature transform
        di_map = {k:{1:'Yes',0:'No'} for k in ['revasc','stchange']}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'death', 'days')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df

    # --- (i) actg --- #
    def process_actg(self, fn = 'actg'):
        df = load_rda(self.dir_process, '%s.rda' % fn)
        cn_fac = ['tx', 'txgrp', 'strat2', 'sex', 'raceth', 'ivdrug', 'hemophil']
        cn_num = ['karnof', 'cd4', 'priorzdv', 'age']
        # (iii) Feature transform
        df[cn_fac] = df[cn_fac].astype(int)
        di_map = {'tx':{1:'IDV',0:'Control'}, 'txgrp':{1:'ZDV+3TC',2:'ZDV+3TC+IDV',3:'d4T+3TC',4:'d4T+3TC+IDV'}, 'sex':{0:'M',1:'F'}, 'strat2':{0:'CD4<=50',1:'CD4>50'}, 'raceth':{1:'White Non-Hispanic', 2:'Black Non-Hispanic', 3:'Hispanic', 4:'Asian, Pacific Islander', 5:'American Indian, Alaskan Native', 6:'Other/unknown'}, 'ivdrug':{1:'Never',2:'Currently',3:'Previously'}, 'hemophil':{1:'Y',0:'N'}}
        self.df_map(df, di_map)
        self.float2int(df)  # Floats to integers
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'censor', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
