# External imports
import os
import numpy as np
import pandas as pd
# Internal imports
from .funs_support import str_subset, try_df_to_int, try_df_to_num, \
    is_subset, ensure_uniform_category


class baseline():
    def __init__(self, dir_pickles, cn_surv, cn_surv2, pkg=None, dir_pkgs=None, dir_custom=None):
        """
        pkg:                Name of R package downloaded
        dir_pkgs:           Folder name where R packages were downloaded
        dir_pickles:         Folder where output should be stored
        cn_surv:            Column names of core survival columns
        cn_surv2:           Includes second time element of cn_surv
        """
        assert (pkg == None) == (dir_pkgs == None), 'if pkg is (not) None, dir_pkgs must be (not) None'
        assert (dir_pkgs == None) != (dir_custom == None), 'Either dir_pkgs OR dir_custom must be None'
        if dir_pkgs != None:
            self.dir_process = os.path.join(dir_pkgs, pkg, 'data')
        else:
            self.dir_process = os.path.join(dir_custom)
        assert os.path.exists(self.dir_process), \
            f'Directory {self.dir_process} does not exist. Please check the path.'
        self.dir_pickles = dir_pickles
        self.cn_surv = cn_surv
        self.cn_surv2 = cn_surv2
    

    def ensure_categorical_commonality(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure that all categorical columns have the same categories.
        This is important for downstream processing and analysis.
        """
        assert isinstance(df, pd.DataFrame)
        cn_fac = df.columns[df.columns.str.startswith('fac_')]
        if len(cn_fac) > 0:
            for cn in cn_fac:
                df[cn] = ensure_uniform_category(df[cn])
        return df
    

    def run_all(self):
        """Wrapper to run through all the process_{} methods in the inheriting class"""
        # Get list of process functions
        methods = str_subset(pd.Series(dir(self)), '^process\\_')
        for method in methods:
            fun_process = getattr(self, method)
            fn, df = fun_process()
            self.write_pickle(fn, df)


    def Surv(self, df, cn_num, cn_fac, cn_event, cn_time, cn_time2=None, cn_pid=None):
        """
        Create the Surv-style columns
        df:                 DataFrame with processed data
        cn_event:           Column name for event binary event indicator
        cn_time:            Column name for time-to-event
        cn_time2:           Interval end for cn_time (which becomes start)
        cn_pid:             Column name for patient ID
        cn_num:             List of columns that are numeric
        cn_fac:             List of columns that are factors
        """
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

    def write_pickle(self, fn:str , 
                  df: pd.DataFrame,
                  allow_overwrite: bool = False,
                  ):
        '''Wrapper for writing to pickle'''
        # Check input name
        assert isinstance(fn, str), 'fn must be a string'
        if fn.endswith('.csv'):
            fn = fn.replace('.csv','.pickle')
        else:
            if not fn.endswith('.pickle'):
                fn = f'{fn}.pickle'        
        
        # Check if the output file exists
        path_write = os.path.join(self.dir_pickles, fn)
        if os.path.exists(path_write):
            old_df = pd.read_pickle(path_write)
            check1 = old_df.equals(df)
            check2 = old_df.dtypes.eq(df.dtypes).all()
            is_same = check1 and check2
            if is_same:
                print(f'File {fn} already exists and is identical to the new DataFrame. Skipping write.')
            else:
                if allow_overwrite:
                    print(f'File {fn} already exists and will be overwritten.')
                    df.to_pickle(path_write, )
                else:
                    print(f'File {fn} already exists. Skipping write.')
        else:
            print(f'Writing DataFrame to {path_write}')
            df.to_pickle(path_write, )


    @staticmethod
    def df_map(df, di_map):
        """
        Map values of a column to new value
        df:         DataFrame to be mapped
        di_map:     Dictionary where keys are column names and values are mapping dict
        """
        df = df.copy()
        assert isinstance(df, pd.DataFrame)
        for cn, di in di_map.items():
            df[cn] = df[cn].map(di).copy()
            assert df[cn].notnull().any(), 'mapping for %s missed a value' % cn

    @staticmethod
    def df_rename(df, di, errors='ignore'):
        '''Wrapper for column rename'''
        assert isinstance(df, pd.DataFrame)
        df.rename(columns=di, inplace=True, errors=errors)

    @staticmethod
    def add_pid(df, cn='pid'):
        '''Add row ids'''
        assert isinstance(df, pd.DataFrame)
        df.insert(0, cn, range(1,len(df)+1))

    def fill_fac(self, df, missing='missing'):
        """
        Fill missing factors
        df:         DataFrame with factor columns
        """ 
        df = df.copy()
        assert isinstance(df, pd.DataFrame)
        cn_df = df.columns
        # (i) Find out which are categorical
        df_dt = df.dtypes
        cidx_cat = df_dt.astype(str) == 'category'
        cols_noncat = df_dt[~cidx_cat].index.to_list()
        cidx_float = df_dt == float
        cols_float = df_dt[cidx_float].index.to_list()
        # (ii) If there are floats, try to convert them to integers
        if len(cols_float) > 0:
            z1 = df[cols_float].apply(self.num2int)
            df[cols_float] = z1.values
        # (iii) If there are non-categorical columns, assign them as categorical
        if len(cols_noncat) > 0:
            z2 = df[cols_noncat].astype('category', copy=True,)
            df = pd.concat(objs=[z2, df.drop(columns=cols_noncat)], axis=1)
        # (iv) Identify the columns which have missing values, and then add the {missing} value to the categories
        cidx_null = df.isnull().any(axis=0)
        cn_null = cidx_null[cidx_null].index.to_list()
        if len(cn_null) > 0:
            # Ensure that the missing value is added to the categories
            df[cn_null] = df[cn_null].apply(lambda x: x.cat.add_categories(missing))
            # Fill the missing values with the {missing} value
            df[cn_null] = df[cn_null].fillna(missing)
        # Return with the original column order
        return df[cn_df]

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
        # Make sure that categories are categorical and missing values are handled
        if len(cn_fac) > 0:
            cn_fac_new = 'fac_'+pd.Series(cn_fac)
            old_fac_df = res[cn_fac_new].copy()
            new_fac_df = self.fill_fac(old_fac_df)
            assert old_fac_df.shape[1] == new_fac_df.shape[1], \
                'Number of columns in old and new factor DataFrame do not match'
            # Add back onto
            res = pd.concat(objs=[res.drop(columns=cn_fac_new), new_fac_df], axis=1)
        # Replace any periods with underscores
        res.columns = res.columns.str.replace('\\.','_',regex=True)
        cn_orig = sum([v for v in di_cn.values() if v is not None],[])
        cn_keep = cn_df[~cn_df.isin(cn_orig)]
        if len(cn_keep) > 0:
            res = pd.concat(objs=[df[cn_keep], res], axis=1)
        return res

    @staticmethod
    def check_num_fac(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convenience wrapper to check that the numeric and factor columns are in the expected format.
        """
        cols_fac = df.columns[df.columns.str.contains('^fac',regex=True)]
        assert df[cols_fac].dtypes.eq('category').all(), 'should be categories'
        assert df[cols_fac].notnull().all().all(), 'there should not be missing values'
        # Check that the numerics are either floats or ints, and if not adjust them
        cols_num = df.columns[df.columns.str.contains('^num',regex=True)]
        dt_num_pre = df[cols_num].dtypes
        if ((dt_num_pre == float) | (dt_num_pre == int)).all():
            pass
        else:
            # Trying to get the correct data type
            dat_num_int = try_df_to_int(df[cols_num], inplace=False)
            assert dat_num_int.shape[1] == len(cols_num), 'expected same number of cols!'
            dt_num_post = dat_num_int.dtypes
            cidx_issue = dt_num_post[~((dt_num_post == float) | (dt_num_post == int))]
            if cidx_issue.any():
                cols_issue = cidx_issue.index.to_list()
                dat_num_int[cols_issue] = try_df_to_num(dat_num_int[cols_issue])
            assert ((dat_num_int.dtypes == float) | (dat_num_int.dtypes == int)).all(), 'should be floats or ints after'
            # Re-combinte the data
            df = pd.concat(objs=[df.drop(columns=cols_num), dat_num_int], axis=1)
        return df
    

    def check_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Will try to make sure that the survival columns are integers in the right format
        """
        # Input checks
        assert isinstance(df, pd.DataFrame)
        cols_df = df.columns.to_list()
        is_surv = is_subset(self.cn_surv, cols_df)
        is_surv2  = is_subset(self.cn_surv2, cols_df)
        assert is_surv or is_surv2, 'Survival columns must be present in the DataFrame'
        surv_cols = self.cn_surv
        if is_surv2:
            surv_cols = self.cn_surv2
        # Create a holder
        df_new = df.copy()
        df_surv_cols = df_new[surv_cols].copy()
        df_new.drop(columns=surv_cols, inplace=True)
        # Find the elible number-like columns
        cn_surv_num = df_surv_cols.select_dtypes(include='number').columns.tolist()
        for cn_num in cn_surv_num:
            # Attempt to convert the survival columns to integers/floats
            df_surv_cols[cn_num] = try_df_to_num(df_surv_cols[[cn_num]])[cn_num]
            # Re-combine 
        df_new = pd.concat(objs=[df_surv_cols, df_new], axis=1)
        return df_new


    # If a column can be converted to integer, do so (assignment happens inplace)
    @staticmethod
    def float2int(df):
        assert isinstance(df, pd.DataFrame)
        cn_float = df.columns[df.dtypes == float]
        if len(cn_float) > 0:
            cn_int = cn_float[np.all(df[cn_float] == df[cn_float].fillna(-99).astype(int),0)]
            df[cn_int] = df[cn_int].astype(int)