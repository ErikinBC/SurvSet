"""
Tests the SurvSet package by fitting a simple elastic-net cox model on all the datasets and storing the concordance.

# Usage:
>>> python3 -m simulation
"""

def main():
    # Standard imports
    import os
    import pandas as pd
    import plotnine as pn
    # linelines imports
    from lifelines import CoxTimeVaryingFitter
    # sksurv imports
    from sksurv.util import Surv as surv_util
    from sksurv.linear_model import CoxnetSurvivalAnalysis
    # sklearn imports for data preprocessing
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.compose import make_column_selector, ColumnTransformer
    # SurvSet package imports
    from SurvSet.data import SurvLoader
    from simulation import stratified_group_split, bootstrap_concordance_index


    ###############################
    # --- (1) PARAMETER SETUP --- #

    # Save to the examples directory
    dir_base = os.getcwd()
    dir_sim = os.path.join(dir_base, 'simulation', )
    print('Figure will saved here: %s' % dir_sim)

    # Concordance empirical alpha level
    alpha = 0.1
    # Number of bootstrap samples
    n_bs = 250
    # Set the random seed
    seed = 1234
    # Percentage of data to use for testing
    test_frac = 0.3


    #####################################
    # --- (2) ENCODER/MODEL/LOADER --- #

    # (i) Set up feature transformer pipeline
    enc_fac = Pipeline(steps=[('ohe', OneHotEncoder(drop=None,sparse_output=False, handle_unknown='ignore'))])
    sel_fac = make_column_selector(pattern='^fac\\_')
    enc_num = Pipeline(steps=[('impute', SimpleImputer(strategy='median')), 
                            ('scale', StandardScaler())])
    sel_num = make_column_selector(pattern='^num\\_')
    # Combine both
    enc_df = ColumnTransformer(transformers=[('ohe', enc_fac, sel_fac),('s', enc_num, sel_num)])
    enc_df.set_output(transform='pandas')  # Ensure output is a DataFrame

    # (ii) Run on datasets
    senc = surv_util()
    loader = SurvLoader()

    # (iii) Set up the models
    mdl_td = CoxTimeVaryingFitter(penalizer=0.1)
    mdl_static = CoxnetSurvivalAnalysis(normalize=True)
    di_mdl = {
        'td': mdl_td,
        'static': mdl_static
    }


    ##################################
    # --- (3) LOOP OVER DATASETS --- #

    # (i) Initialize results holder and loop over datasets
    n_ds = len(loader.df_ds)
    holder_cindex = []
    for i, r in loader.df_ds.iterrows():
        is_td, ds = r['is_td'], r['ds']
        print('Dataset %s (%i of %i)' % (ds, i+1, n_ds))
        df = loader.load_dataset(ds)['df']
        # Split based on both the event rate and unique IDs
        df_train, df_test = stratified_group_split(df=df, group_col='pid', 
                                stratify_col='event', test_frac=test_frac, seed=seed)
        assert not df_train['pid'].isin(df_test['pid']).any(), \
            'Training and test sets must not overlap in patient IDs.'
        # Fit encoder
        enc_df.fit(df_train)
        # Transform data
        X_train = enc_df.transform(df_train)
        assert X_train.columns.str.split('\\_{1,2}', expand=True).to_frame(False)[1].isin(['fac','num']).all(), 'Expected feature names to be prefixed with "fac_" or "num_"'
        X_test = enc_df.transform(df_test)
        # Set up the survival object and fit the model depending on whether time-dependent or not
        mdl = di_mdl['td'] if is_td else di_mdl['static']
        if is_td:
            # Add on the labels to the training data
            X_train = pd.concat(objs=[df_train[['pid','event','time','time2']], X_train],axis=1)
            # Fit
            mdl.fit(X_train, id_col="pid", event_col="event", start_col="time", stop_col="time2", show_progress=False)
            # Get test prediction
            scores_test = mdl.predict_partial_hazard(X_test).values
        else:
            # Set up Surv object for static model and fit
            So_train = senc.from_arrays(df_train['event'].astype(bool), df_train['time'])
            mdl.fit(X=X_train, y=So_train)
            # Get test prediction
            scores_test = mdl.predict(X_test)
        # Prepare test data for concordance calculation
        res_test = df_test[['pid','event','time']].assign(scores=scores_test)
        if is_td:
            res_test['time2'] = df_test['time2'].values
        # Generate results and bootstrap concordance index
        res_cindex = bootstrap_concordance_index(res_test, 'pid', 'event', 'time', 'scores', 'time2', n_bs, alpha, is_td=is_td)
        res_cindex.insert(0, 'ds', ds) 
        res_cindex.insert(1, 'is_td', is_td)  # Add dataset and type
        holder_cindex.append(res_cindex)

    # (ii) Merge results
    df_cindex = pd.concat(holder_cindex, ignore_index=True, axis=0)
    ds_ord = df_cindex.sort_values('cindex')['ds'].values
    df_cindex['ds'] = pd.Categorical(df_cindex['ds'], ds_ord)
    

    ############################
    # --- (4) PLOT RESULTS --- #

    # (i) Plot concordance index
    gg_cindex = (pn.ggplot(df_cindex, pn.aes(y='cindex',x='ds', color='is_td')) + 
        pn.theme_bw() + pn.coord_flip() + 
        pn.geom_point(size=2) + 
        pn.geom_linerange(pn.aes(ymin='lb', ymax='ub')) + 
        pn.labs(y='Concordance') + 
        pn.scale_color_discrete(name='Time-varying covariates') +
        pn.geom_hline(yintercept=0.5,linetype='--', color='black') + 
        pn.theme(axis_title_y=pn.element_blank()))
    path_fig = os.path.join(dir_sim, 'gg_cindex.png')
    gg_cindex.save(path_fig, height=10, width=5)


    print('~~~ The SurvSet.sim_run module was successfully executed ~~~')


if __name__ == '__main__':
    # Call the main module
    main()