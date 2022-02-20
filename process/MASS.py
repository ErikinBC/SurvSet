# Processe the MASS package
import numpy as np
from funs_class import baseline
from funs_support import load_rda, df_map, add_suffix

# (i) Create event, time, and id
# (ii) Subset
# (iii) Feature transform
# (iv) Define num, fac, and Surv
# (v) Write

class package(baseline):
    # --- (i) AIDS2 --- #
    def process_aids2(self):
        df = load_rda(self.dir_process, 'Aids2.rda')
        cn_fac = ['state','sex','T.categ']
        cn_num = ['age']
        # (i) Create event, time, and id
        df = df.assign(time=lambda x: x['death']-x['diag'])
        df['status'] = df['status'].map({'D':1, 'A':0}).astype(int)
        # (ii) Subset
        df = df.drop_duplicates()
        # (iii) Feature transform
        # (iv) Define Surv, and rename
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='time')
        df = add_suffix(df, cn_num, cn_fac)
        # (v) Write
        self.write_csv('aids2.csv', df)


    # # --- (ii) MELANOMA --- #
    def process_melanoma(self):
        df = load_rda(self.dir_process, 'Melanoma.rda')
        cn_fac = ['sex', 'ulcer']
        cn_num = ['age', 'year', 'thickness']
        # (i) Create event, time, and id
        df['status'] = np.where(df['status']==1, 1, 0)
        # (ii) Subset
        # (iii) Feature transform
        di_map = {'sex':{1:'M', 0:'F'}, 'ulcer':{1:'presence', 0:'absense'}}
        df_map(df, di_map)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, cn_event='status', cn_time='time')        
        df = add_suffix(df, cn_num, cn_fac)
        # (v) Write
        self.write_csv('melanoma.csv', df)


# cn_surv = ['pid', 'time', 'event']
# cn_surv2 = ['pid', 'time', 'time2', 'event']
# dir_base = os.getcwd()
# dir_output = os.path.join(dir_base, 'output')
# dir_pkgs = os.path.join(dir_base, 'pkgs')
# self = package(pkg='MASS', dir_pkgs=dir_pkgs, dir_output=dir_output, cn_surv=cn_surv, cn_surv2=cn_surv2)

