# Process coxphf datasets
import os
import pandas as pd
from funs_class import baseline

class package(baseline):
    # --- (i) breast --- #
    def process_breast(self, fn = 'breast'):
        path = os.path.join(self.dir_process, '%s.txt' % fn)
        df = pd.read_csv(path, sep='\\s{1,}', engine='python')
        cn_fac = ['T','N','G','CD']
        cn_num = []
        df = df.drop_duplicates()
        # (iii) Feature transform
        di_map = {k:{1:'Unfavourable', 0:'Favourable'} for k in cn_fac}
        self.df_map(df, di_map)
        # (iv) Define Surv, and rename
        df = self.Surv(df, cn_num, cn_fac, 'CENS', 'TIME')
        df = self.add_suffix(df, cn_num, cn_fac)
        di_cn = {'T':'TumorStage', 'N':'NodalStatus', 'G':'Histology','CD':'CathepsinD'}
        di_cn = {'fac_'+k:'fac_'+v for k,v in di_cn.items()}
        self.df_rename(df, di_cn)
        return fn, df
