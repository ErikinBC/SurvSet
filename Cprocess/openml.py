# Process openml datasets
import os
import pandas as pd
from funs_class import baseline
from funs_support import str_subset

class package(baseline):
    # --- (i) phpl04K8a --- #
    def process_phpl04K8a(self, fn = 'phpl04K8a'):
        path = os.path.join(self.dir_process, 'phpl04K8a.csv')
        df = pd.read_csv(path)
        cn_fac = ['sex']
        cn_num = ['age'] + list(str_subset(df.columns,'^g'))        
        # (i) Create event, time, and id
        df['OS_event']= df['OS_event'].str.replace('[^0-9]','',regex=True).astype(int)
        # (iii) Feature transform
        df['sex']= df['sex'].str.replace('[^a-z]','',regex=True)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'OS_event', 'OS_years')
        df = self.add_suffix(df, cn_num, cn_fac)
        return fn, df
