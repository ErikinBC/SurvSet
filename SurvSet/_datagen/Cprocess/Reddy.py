# Process Chandan Reddy datasets
import os
import pandas as pd
from funs_class import baseline


class package(baseline):

    # All four datasets have the same format
    def clean_df(self, fn):
        fold = os.path.join(self.dir_process, 'Gene_expression_data')
        path = os.path.join(fold, '%s.csv' % fn)
        df = pd.read_csv(path)
        # First three columns are time, event, ignore
        cn_df = df.columns
        cn_A = cn_df[3:]
        n_A = len(cn_A)
        cn_gene = 'gene_'+pd.Series(range(1,n_A+1)).astype(str)
        di_cn = dict(zip(cn_A, cn_gene))
        self.df_rename(df, di_cn)
        df.rename(columns=dict(zip(cn_df[:3],['time','event','drop'])), inplace=True)
        cn_fac = []
        cn_num = list(cn_gene)
        # (iv) Define num, fac, and Surv
        df = self.Surv(df, cn_num, cn_fac, 'event', 'time')
        df = self.add_suffix(df, cn_num, cn_fac)
        return df

    # --- (i) NSBCD --- #
    def process_NSBCD(self, fn = 'NSBCD'):
        df = self.clean_df(fn)
        return fn, df

    # --- (ii) AML_Bull --- #
    def process_AMLBull(self, fn = 'AML_Bull'):
        df = self.clean_df(fn)
        return fn, df

    # --- (iii) DBCD --- #
    def process_DBCD(self, fn = 'DBCD'):
        df = self.clean_df(fn)
        return fn, df

    # --- (iv) DLBCL --- #
    def process_(self, fn = 'DLBCL'):
        df = self.clean_df(fn)
        return fn, df

