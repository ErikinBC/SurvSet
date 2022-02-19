
# Load modules
import os
import numpy as np
import pandas as pd
from funs_class import baseline
from funs_support import load_rda, rename_cols, add_pid

class package(baseline):
    # --- (i) AIDS2 --- #
    def process_aids2(self):
        df_aids2 = load_rda(self.dir_process, 'Aids2.rda')
        # (i) Create the event time
        df_aids2 = df_aids2.assign(time=lambda x: x['death']-x['diag'])
        df_aids2 = df_aids2.assign(event=lambda x: x['status'].map({'D':1, 'A':0}))
        # (ii) Drop duplicates
        df_aids2 = df_aids2.drop_duplicates()
        # (iii) Clean up
        add_pid(df_aids2)
        cn_fac = ['state','sex','T.categ']
        cn_num = ['age']
        df_aids2 = df_aids2[self.cn_surv + cn_num + cn_fac]
        df_aids2 = rename_cols(df_aids2 , cn_num, cn_fac)
        df_aids2.reset_index(drop=True, inplace=True)
        # (iv) Save
        path_write = os.path.join(self.dir_output, 'aids2.csv')
        df_aids2.to_csv(path_write, index=False)

    # # --- (ii) MELANOMA --- #
    def process_melanoma(self):
        df_mela = load_rda(self.dir_process, 'Melanoma.rda')
        # (i) Only death from melanoma as event
        df_mela = df_mela.assign(event=lambda x: np.where(x['status']==1, 1, 0))
        # (ii) Clean up
        add_pid(df_mela)
        cn_fac = []
        cn_num = ['sex', 'ulcer', 'age', 'year', 'thickness']
        df_mela = df_mela[self.cn_surv + cn_num + cn_fac]
        df_mela = rename_cols(df_mela , cn_num, cn_fac)
        # (iii) Save
        path_write = os.path.join(self.dir_output, 'melanoma.csv')
        df_mela.to_csv(path_write, index=False)

