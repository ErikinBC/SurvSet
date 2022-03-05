import os
import numpy as np
import pandas as pd
import plotnine as pn
from pathlib import Path
from SurvSet.data import SurvLoader
from sksurv.util import Surv
from sksurv.metrics import concordance_index_censored as concordance
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_selector
from sklearndf.pipeline import PipelineDF
from sklearndf.transformation import OneHotEncoderDF, ColumnTransformerDF, SimpleImputerDF, StandardScalerDF

dir_tests = Path(__file__).parent
print('Figure will saved here: %s' % dir_tests)

# (i) Set up feature transformer pipeline
enc_fac = PipelineDF(steps=[('ohe', OneHotEncoderDF(sparse=False, drop=None, handle_unknown='ignore'))])
sel_fac = make_column_selector(pattern='^fac\\_')
enc_num = PipelineDF(steps=[('impute', SimpleImputerDF(strategy='median')), ('scale', StandardScalerDF())])
sel_num = make_column_selector(pattern='^num\\_')
# Combine both
enc_df = ColumnTransformerDF(transformers=[('ohe', enc_fac, sel_fac),('s', enc_num, sel_num)])

# (ii) Run on datasets
alpha = 0.1
senc = Surv()
loader = SurvLoader()
ds_lst = loader.df_ds[~loader.df_ds['is_td']]['ds'].to_list()  # Remove datasets with time-varying covariates
n_ds = len(ds_lst)
holder_cindex = np.zeros([n_ds, 3])
for i, ds in enumerate(ds_lst):
    print('Dataset %s (%i of %i)' % (ds, i+1, n_ds))
    anno = loader.df_ds.query('ds == @ds').T.to_dict()
    anno = anno[list(anno)[0]]
    df, ref = loader.load_dataset(ds).values()
    # Random stratified split
    df_train, df_test = train_test_split(df, stratify=df['event'], random_state=1, test_size=0.3)
    # Fit encoder
    enc_df.fit(df_train)
    # Sanity check
    cn_prefix = enc_df.feature_names_original_.str.split('_',1,True)[0].unique()
    assert all([cn in ['fac', 'num'] for cn in cn_prefix])
    # Prepare numpy arrays
    X_train = enc_df.transform(df_train)
    So_train = senc.from_arrays(df_train['event'].astype(bool), df_train['time'])
    X_test = enc_df.transform(df_test)
    # Fit model
    mdl = CoxnetSurvivalAnalysis(normalize=True)
    mdl.fit(X=X_train, y=So_train)
    scores_test = mdl.predict(X_test)
    res_test = df_test[['event','time']].assign(scores=scores_test)
    So_test = senc.from_arrays(res_test['event'].astype(bool), res_test['time'])
    conc_test = concordance(So_test['event'], So_test['time'], res_test['scores'])[0]
    # Get concordance
    n_bs = 250
    holder_bs = np.zeros(n_bs)
    for j in range(n_bs):
        res_bs = res_test.groupby(['event']).sample(frac=1,replace=True,random_state=j)
        So_bs = senc.from_arrays(res_bs['event'].astype(bool), res_bs['time'])
        conc_bs = concordance(So_bs['event'], So_bs['time'], res_bs['scores'])[0]
        holder_bs[j] = conc_bs
    lb, ub = np.quantile(holder_bs, [alpha,1-alpha])
    holder_cindex[i] = [conc_test, lb, ub]

# (iii) Merge results & plot
df_cindex = pd.DataFrame(holder_cindex, columns=['cindex', 'lb', 'ub'])
df_cindex.insert(0, 'ds', ds_lst)
ds_ord = df_cindex.sort_values('cindex')['ds'].values
df_cindex['ds'] = pd.Categorical(df_cindex['ds'], ds_ord)

gg_cindex = (pn.ggplot(df_cindex, pn.aes(y='cindex',x='ds')) + 
    pn.theme_bw() + pn.coord_flip() + 
    pn.geom_point(size=2) + 
    pn.geom_linerange(pn.aes(ymin='lb', ymax='ub')) + 
    pn.labs(y='Concordance') + 
    pn.geom_hline(yintercept=0.5,linetype='--', color='red') + 
    pn.theme(axis_title_y=pn.element_blank()))
gg_cindex.save(os.path.join(dir_tests, 'gg_cindex.png'), height=10, width=5)
