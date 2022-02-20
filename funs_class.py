# Baseline class to be used by all package processing scripts
import os
import pandas as pd

"""
pkg:
dir_pkgs:
dir_output:
cn_surv:
cn_surv2:
"""
class baseline():
    def __init__(self, pkg, dir_pkgs, dir_output, cn_surv, cn_surv2):
        self.dir_process = os.path.join(dir_pkgs, pkg, 'data')
        self.dir_output = dir_output
        self.cn_surv = cn_surv
        self.cn_surv2 = cn_surv2

    
    """Create the Surv-style columns
    df
    cn_event
    cn_time
    cn_time2
    cn_pid
    cn_num
    cn_fac
    """
    def Surv(self, df, cn_num, cn_fac, cn_event, cn_time, cn_time2=None, cn_pid=None):
        assert isinstance(df, pd.DataFrame)
        cn_df = list(df.columns)
        assert cn_event in cn_df, 'cn_event not found in cn_df'
        assert cn_time in cn_df, 'cn_time not found in cn_df'
        di_Surv = {cn_event:'event', cn_time:'time', cn_time2:'time2', cn_pid:'pid'}
        df = df.rename(columns=di_Surv, errors='ignore')
        n_df = len(df)
        if cn_pid is None:
            df.insert(0, 'pid', range(n_df))
        else:
            assert cn_pid in cn_df, 'cn_pid not found in cn_df'
        cn_surv = [v for k,v in di_Surv.items() if k is not None]
        df = df[cn_surv + cn_num+cn_fac]
        df.reset_index(drop=True, inplace=True)
        return df

    def write_csv(self, fn, df):
        path_write = os.path.join(self.dir_output, fn)
        df.to_csv(path_write, index=False)