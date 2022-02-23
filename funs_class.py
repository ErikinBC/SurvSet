# Baseline class to be used by all package processing scripts
import os
import numpy as np
import pandas as pd

"""
pkg:                Name of R package downloaded
dir_pkgs:           Folder name where R packages were downloaded
dir_output:         Folder where output should be stored
cn_surv:            Column names of core survival columns
cn_surv2:           Includes second time element of cn_surv
"""
class baseline():
    def __init__(self, pkg, dir_pkgs, dir_output, cn_surv, cn_surv2):
        self.dir_process = os.path.join(dir_pkgs, pkg, 'data')
        self.dir_output = dir_output
        self.cn_surv = cn_surv
        self.cn_surv2 = cn_surv2

    
    """Create the Surv-style columns
    df:                 DataFrame with processed data
    cn_event:           Column name for event binary event indicator
    cn_time:            Column name for time-to-event
    cn_time2:           Interval end for cn_time (which becomes start)
    cn_pid:             Column name for patient ID
    cn_num:             List of columns that are numeric
    cn_fac:             List of columns that are factors
    """
    def Surv(self, df, cn_num, cn_fac, cn_event, cn_time, cn_time2=None, cn_pid=None):
        assert isinstance(df, pd.DataFrame)
        cn_df = list(df.columns)
        assert cn_event in cn_df, 'cn_event not found in cn_df'
        assert cn_time in cn_df, 'cn_time not found in cn_df'
        di_Surv = {cn_pid:'pid', cn_event:'event', cn_time:'time', cn_time2:'time2'}
        df = df.rename(columns=di_Surv, errors='ignore')
        n_df = len(df)
        if cn_pid is None:
            df.insert(0, 'pid', range(n_df))
        else:
            assert cn_pid in cn_df, 'cn_pid not found in cn_df'
        cn_surv = [v for k,v in di_Surv.items() if k is not None]
        df = df[cn_surv + cn_num + cn_fac]
        df.reset_index(drop=True, inplace=True)
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
    def fill_fac(self, df):
        assert isinstance(df, pd.DataFrame)
        # Check to see whether non-missing factors can be made to integers
        cn_dtypes = df.apply(lambda x: x.dropna().unique().dtype,0)
        cn_float = df.columns[np.where(cn_dtypes == float)[0]]
        if len(cn_float) > 0:
            holder = []
            for cn in cn_float:
                holder.append(self.num2int(df[cn]))
            z = pd.concat(holder,axis=1)
            # z = df[cn_float].apply(self.num2int(df[cn_float]))
            df = pd.concat(objs=[z, df.drop(columns=cn_float)],axis=1)
        df = df.fillna('missing')
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
    @staticmethod
    def add_suffix(df, cn_num=None, cn_fac=None):
        assert isinstance(df, pd.DataFrame)
        cn_df = df.columns
        di_cn = {'num':cn_num, 'fac':cn_fac}
        for k, v in di_cn.items():
            if v is not None:
                if isinstance(v, str):
                    v = [v]
                    di_cn[k] = v
                cn_err = np.setdiff1d(v, cn_df)
                assert len(cn_err)==0, 'Columns %s from %s were not found in columns' % (cn_err,k)
                di_v = dict(zip(v,['%s_%s'%(k,cn) for cn in v]))
                df = df.rename(columns=di_v)
        # Replace any periods with underscores
        df.columns = df.columns.str.replace('\\.','_',regex=True)
        return df

    # If a column can be converted to integer, do so (assignment happens inplace)
    @staticmethod
    def float2int(df):
        assert isinstance(df, pd.DataFrame)
        cn_float = df.columns[df.dtypes == float]
        if len(cn_float) > 0:
            cn_int = cn_float[np.all(df[cn_float] == df[cn_float].fillna(-99).astype(int),0)]
            df[cn_int] = df[cn_int].astype(int)