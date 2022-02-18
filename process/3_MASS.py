dir_pkgs = os.path.join(dir_base, 'pkgs')

# Load modules
import os
import numpy as np
import pandas as pd
from funs_support import makeifnot, load_rda, rename_cols




dir_process = os.path.join(dir_pkgs, 'MASS', 'data')


# Baseline columns for all datasets
cn_surv = ['pid', 'time', 'time2', 'event']


#####################
# --- (i) AIDS2 --- #

# This should be a funs_support function
df_aids2 = load_rda(dir_process, 'Aids2.rda')
# (i) Create the event time
df_aids2 = df_aids2.assign(time=lambda x: x['death']-x['diag'])
df_aids2 = df_aids2.assign(event=lambda x: x['status'].map({'D':1, 'A':0}))
# (ii) Drop duplicates
df_aids2 = df_aids2.drop_duplicates()
# (iii) Insert needed columns
df_aids2.insert(0, 'time2', np.nan)
df_aids2.insert(0, 'pid', range(len(df_aids2)))
# (iv) Clean up
cn_fac = ['state','sex','T.categ']
cn_num = ['age']
df_aids2 = df_aids2[cn_surv + cn_num + cn_fac]
df_aids2 = rename_cols(df_aids2 , cn_num, cn_fac)
df_aids2.to_csv(os.path.join(dir_output, 'aids2.csv'))


#########################
# --- (ii) MELANOMA --- #




