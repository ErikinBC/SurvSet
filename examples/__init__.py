"""
Contains the functions that mimic the code in the README
"""

def example_simple() -> None:
    from SurvSet.data import SurvLoader
    loader = SurvLoader()
    # List of available datasets and meta-info
    print(loader.df_ds.head())
    # Load dataset and its reference
    df, ref = loader.load_dataset(ds_name='ova').values()
    print(df.head())


def example_complex() -> None:
    # Modules needed for fitting
    import pandas as pd
    from sksurv.util import Surv
    from lifelines import CoxTimeVaryingFitter
    from sksurv.linear_model import CoxnetSurvivalAnalysis
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import make_column_selector, ColumnTransformer
    # Set up the dataset loader
    from SurvSet.data import SurvLoader
    loader = SurvLoader()
    
    # (i) Set up a pipeline to handle numerical (possibly missing) and categorical features 
    enc_fac = Pipeline(steps=[('ohe', OneHotEncoder(drop=None,sparse_output=False, handle_unknown='ignore'))])
    sel_fac = make_column_selector(pattern='^fac\\_')
    enc_num = Pipeline(steps=[('impute', SimpleImputer(strategy='median')), 
                            ('scale', StandardScaler())])
    sel_num = make_column_selector(pattern='^num\\_')
    enc_df = ColumnTransformer(transformers=[('ohe', enc_fac, sel_fac),('s', enc_num, sel_num)])
    enc_df.set_output(transform='pandas')

    # (ii) Non-time-varying dataset (prostate)
    df_prostate = loader.load_dataset(ds_name='prostate')['df']
    # Set up data and model
    senc = Surv()
    So = senc.from_arrays(df_prostate['event'].astype(bool), df_prostate['time'])
    enc_df.fit(df_prostate)
    X_train = enc_df.transform(df_prostate)
    mdl = CoxnetSurvivalAnalysis(n_alphas=50, )
    # Fit and predict
    mdl.fit(X=X_train, y=So)
    mdl.predict(X_train)

    # (ii) Load a time-varying dataset (epileptic)
    df_epileptic = loader.load_dataset(ds_name='epileptic')['df']
    # Set up data and model
    mdl = CoxTimeVaryingFitter(penalizer=0.1)
    enc_df.fit(df_epileptic)
    X_train = enc_df.transform(df_epileptic)
    X_train = pd.concat(objs=[df_epileptic[['pid','event','time','time2']], X_train], axis=1)

    # Fit an predict
    mdl.fit(X_train, id_col="pid", event_col="event", start_col="time", stop_col="time2", show_progress=False)
    # Get test prediction
    mdl.predict_partial_hazard(X_train)
