import os
import numpy as np
import pandas as pd
from pathlib import Path
from SurvSet._datagen.funs_ref import di_ref

"""
Main class to load SurvSet datasets
"""
class SurvLoader():
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

    """
    ds_name:            A Survset Dataset
    
    Returns:            A dictionary with elements {'df':pd.DataFrame, 'ref':url}
    """
    def load_dataset(self, ds_name):
        assert ds_name in self.df_ds['ds'].to_list(), '%s not found in dataset directory! See SurvLoader.df_ds["ds"] for a list of valid datasets' % ds_name
        path_ds = os.path.join(self.fold_ds, ds_name+'.csv')
        df = pd.read_csv(path_ds)
        ref = di_ref[ds_name]
        di = {'df':df, 'ref':ref}
        return di