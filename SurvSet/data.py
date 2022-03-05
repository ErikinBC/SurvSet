import os
import numpy as np
import pandas as pd
from pathlib import Path
from SurvSet._datagen.funs_ref import di_ref

class SurvLoader():
    """SurvLoader is the class used to call in SurvSet datasets

    This class has no initialization arguments and can be called as SurvLoader()

    Attributes:
        fold_ds:    Folder where csv files live
        df_ds:      pd.DataFrame with columns: ds (dataset alias), is_td (has time-varying features), n (sample size), n_fac (number of categorical columns), n_ohe (not of one-hot-encoded columns), and n_num (number of continuous columns) 
    """
    def __init__(self):
        # Link to dataset source
        dir_SurvSet = Path(__file__).parent
        fold_datagen = os.path.join(dir_SurvSet, '_datagen')
        self.fold_ds = os.path.join(fold_datagen, 'output')
        lst_csv = pd.Series(os.listdir(self.fold_ds))
        fn_csv = lst_csv.str.replace('\\.csv$','',regex=True)
        # Load pre-calculated dataset information
        self.df_ds = pd.read_csv(os.path.join(fold_datagen, 'figures', 'df_ds.csv'))
        d_csv = np.setdiff1d(fn_csv, self.df_ds['ds'])
        assert len(d_csv) == 0, 'New dataset detected: %s' % list(d_csv)

    def load_dataset(self, ds_name):
        """load_data calls in a dataset

        Parameters:
            ds_name (str): A Survset Dataset

        Returns:            
            A dictionary with elements {'df':pd.DataFrame, 'ref':url}
            
            df has the following columns: pid (unique ID), time (time to event or start time), time2 (None or end tend), num_{} (numeric columns), fac_{} (categorical columns)

            ref is the url which contains the feature description found from the original source
        """
        assert ds_name in self.df_ds['ds'].to_list(), '%s not found in dataset directory! See SurvLoader.df_ds["ds"] for a list of valid datasets' % ds_name
        path_ds = os.path.join(self.fold_ds, ds_name+'.csv')
        df = pd.read_csv(path_ds, low_memory=False, na_values='na')
        ref = di_ref[ds_name]
        # Force categories to string
        cn_df = df.columns
        cn_fac = list(cn_df[cn_df.str.contains('^fac\\_',regex=True)])
        if len(cn_fac) > 0:
            df[cn_fac] = df[cn_fac].astype(str).values
        di = {'df':df, 'ref':ref}
        return di