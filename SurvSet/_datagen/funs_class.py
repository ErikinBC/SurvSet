# Baseline class to be used by all package processing scripts
import os
import numpy as np
import pandas as pd
from funs_support import str_subset

"""
pkg:                Name of R package downloaded
dir_pkgs:           Folder name where R packages were downloaded
dir_output:         Folder where output should be stored
cn_surv:            Column names of core survival columns
cn_surv2:           Includes second time element of cn_surv
"""
class baseline():
    def __init__(self, dir_output, cn_surv, cn_surv2, pkg=None, dir_pkgs=None, dir_custom=None):
        assert (pkg == None) == (dir_pkgs == None), 'if pkg is (not) None, dir_pkgs must be (not) None'
        assert (dir_pkgs == None) != (dir_custom == None), 'Either dir_pkgs OR dir_custom must be None'
        if dir_pkgs != None:
            self.dir_process = os.path.join(dir_pkgs, pkg, 'data')
        else:
            self.dir_process = os.path.join(dir_custom)
        self.dir_output = dir_output
        self.cn_surv = cn_surv
        self.cn_surv2 = cn_surv2

    """
    Wrapper to run through all the process_{} methods in the inheriting class
    """
    def run_all(self):
        # Get list of process functions
        methods = str_subset(pd.Series(dir(self)), '^process\\_')
        for method in methods:
            fun_process = getattr(self, method)
            fn, df = fun_process()
            self.write_csv('%s.csv' % fn, df)

    """Create the Surv-style columns
    df:                 DataFrame with processed data
    cn_event:           Column name for event binary event indicator
    cn_time:            Column name for time-to-event
    cn_time2:           Interval end for cn_time (which becomes start)
    cn_pid:             Column name for patient ID
    cn_num:             List of columns that are numeric
    cn_fac:             List of columns that are factors
    """
    # cn_event,cn_time,cn_time2,cn_pid='pgstat','pgtime',None,None
    def Surv(self, df, cn_num, cn_fac, cn_event, cn_time, cn_time2=None, cn_pid=None):
        assert isinstance(df, pd.DataFrame)
        cn_df = list(df.columns)
        assert cn_event in cn_df, 'cn_event not found in cn_df'
        assert cn_time in cn_df, 'cn_time not found in cn_df'
        di_Surv = {cn_pid:'pid', cn_event:'event', cn_time:'time', cn_time2:'time2'}
        df = df.rename(columns=di_Surv, errors='ignore')
        n_df = len(df)
        if cn_pid is None:
            df = df.assign(pid=range(n_df))
            di_Surv = {**{'pid':'pid'}, **di_Surv}
        else:
            assert cn_pid in cn_df, 'cn_pid not found in cn_df'
            df = df.rename(columns={cn_pid:'pid'})
        cn_surv = [v for k,v in di_Surv.items() if k is not None]
        cn_rest = list(np.unique(cn_num + cn_fac))
        df = df[cn_surv + cn_rest].reset_index(drop=True)
        return df

    # Wrapper for writing to csv
    def write_csv(self, fn, df):
        path_write = os.path.join(self.dir_output, fn)
        df.to_csv(path_write, index=False)

    """Map values of a column to new value
    df:         DataFrame to be mapped
    di_map:     Dictionary where keys are column names and values are mapping dict
    """
    @staticmethod
    def df_map(df, di_map):
        assert isinstance(df, pd.DataFrame)
        for cn, di in di_map.items():
            df[cn] = df[cn].map(di)
            assert df[cn].notnull().any(), 'mapping for %s missed a value' % cn

    # Wrapper for column rename
    @staticmethod
    def df_rename(df, di, errors='ignore'):
        assert isinstance(df, pd.DataFrame)
        df.rename(columns=di, inplace=True, errors=errors)

    # Add row ids
    @staticmethod
    def add_pid(df, cn='pid'):
        assert isinstance(df, pd.DataFrame)
        df.insert(0, cn, range(1,len(df)+1))

    """Fill missing factors
    df:         DataFrame with factor columns
    """
    def fill_fac(self, df, missing='missing'):
        assert isinstance(df, pd.DataFrame)
        cn_df = df.columns
        cn_dtypes = df.apply(lambda x: x.dropna().unique().dtype,0)
        cn_float = cn_df[np.where(cn_dtypes == float)[0]]
        cn_cat = cn_df[np.where(cn_dtypes == 'category')[0]]
        # Check to see whether non-missing factors can be made to integers
        if len(cn_float) > 0:
            z = df[cn_float].apply(self.num2int)
            df = pd.concat(objs=[z, df.drop(columns=cn_float)],axis=1)
        if len(cn_cat) > 0:
            z = df[cn_cat].apply(lambda x: x.cat.add_categories('missing'))
            df = pd.concat(objs=[z, df.drop(columns=cn_cat)],axis=1)
        # Ensure column order is preserved
        df = df.fillna(missing)[cn_df]
        return df

    # Replace missing and make int
    @staticmethod
    def num2int(x, fill='missing'):
        assert isinstance(x, pd.Series)
        mi = int(x.min()-1)
        z = x.fillna(mi).astype(int).astype(str)
        z = z.replace(str(mi),fill)
        return z

    # Add suffix to numerical and factor columns
    def add_suffix(self, df, cn_num=None, cn_fac=None):
        assert isinstance(df, pd.DataFrame)
        cn_df = pd.Series(df.columns)
        di_cn = {'num':cn_num, 'fac':cn_fac}
        holder = []
        for k, v in di_cn.items():
            if v is not None:
                n_v = len(v)
                if n_v > 0:
                    if isinstance(v, str):
                        v = [v]
                        di_cn[k] = v
                    cn_v = pd.Series(v)
                    cn_err = list(cn_v[~cn_v.isin(cn_df)])
                    assert len(cn_err)==0, 'Columns %s from %s were not found in columns' % (cn_err,k)
                    di_cn_v = dict(zip(cn_v, k+'_'+cn_v))
                    holder.append(df[cn_v].rename(columns = di_cn_v))
        res = pd.concat(holder,axis=1)
        # Fill missing values for category
        if len(cn_fac) > 0:
            cn_fac_new = 'fac_'+pd.Series(cn_fac)
            res[cn_fac_new] = self.fill_fac(res[cn_fac_new]).values
        # Replace any periods with underscores
        res.columns = res.columns.str.replace('\\.','_',regex=True)
        cn_orig = sum([v for v in di_cn.values() if v is not None],[])
        cn_keep = cn_df[~cn_df.isin(cn_orig)]
        if len(cn_keep) > 0:
            res = pd.concat(objs=[df[cn_keep], res], axis=1)
        return res

    # If a column can be converted to integer, do so (assignment happens inplace)
    @staticmethod
    def float2int(df):
        assert isinstance(df, pd.DataFrame)
        cn_float = df.columns[df.dtypes == float]
        if len(cn_float) > 0:
            cn_int = cn_float[np.all(df[cn_float] == df[cn_float].fillna(-99).astype(int),0)]
            df[cn_int] = df[cn_int].astype(int)