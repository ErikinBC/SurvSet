"""
Main data loader for SurvSet datasets

# Manual script test:
>>> python3 -m SurvSet.data
"""

# External modules
import pickle
import pandas as pd
import importlib.resources as pkg_resources
# Internal modules
from .utils import di_ref, fn_df_ds


class SurvLoader():
    """SurvLoader is the class used to call in SurvSet datasets

    This class has no initialization arguments and can be called as SurvLoader()

    Attributes:
        fold_ds:    Folder where csv files live
        df_ds:      pd.DataFrame with columns: ds (dataset alias), is_td (has time-varying features), n (sample size), n_fac (number of categorical columns), n_ohe (not of one-hot-encoded columns), and n_num (number of continuous columns) 
    """
    path_to_resources = "SurvSet.resources"
    path_to_data = f"{path_to_resources}.pickles"
    def __init__(self):
        # Load pre-calculated dataset information
        self.df_ds = self.load_csv(fn_df_ds)

    def load_pickle(self, name: str) -> pd.DataFrame:
        '''Method to load the pickle files'''
        pickle_path = pkg_resources.files(self.path_to_data).joinpath(f"{name}.pickle")
        with pickle_path.open("rb") as f:
            return pickle.load(f)

    def load_csv(self, name: str) -> pd.DataFrame:
        '''Method to load the pickle files'''
        fn_safe = name.split('.csv')[0] + '.csv'
        csv_path = pkg_resources.files(self.path_to_data).joinpath(f"{fn_safe}")
        with csv_path.open("rb") as f:
            return pd.read_csv(f)


    def load_dataset(self, ds_name) -> dict:
        """
        load_data calls in a dataset

        Parameters:
            ds_name (str): A Survset Dataset

        Returns:            
            A dictionary with elements {'df':pd.DataFrame, 'ref':url}
            
            df has the following columns: pid (unique ID), time (time to event or start time), time2 (None or end tend), num_{} (numeric columns), fac_{} (categorical columns)

            ref is the url which contains the feature description found from the original source
        """
        assert ds_name in self.df_ds['ds'].to_list(), '%s not found in dataset directory! See SurvLoader().df_ds["ds"] for a list of valid datasets' % ds_name
        # Load the dataset
        df = self.load_pickle(ds_name)
        ref = di_ref[ds_name]
        # Combine dataframe and reference and return
        di = {'df':df, 'ref':ref}
        return di


def _surv_test() -> None:
    # Test the SurvLoader class
    enc = SurvLoader()
    n_ds = len(enc.df_ds)
    df_names = enc.df_ds['ds'].to_list()
    print(f"There are {n_ds:,} available datasets: {df_names}")
    di = enc.load_dataset('ova')
    print('Loaded dataset "ova":', di['df'].head())
    print('Reference URL:', di['ref'])
    # Check for a non-existent dataset
    try:
        di = enc.load_dataset('madeup')
    except AssertionError as e:
        print(e)


if __name__ == '__main__':
    # Call the surv test class
    _surv_test()