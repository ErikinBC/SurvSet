from SurvSet.data import SurvLoader
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_selector
from sklearndf.pipeline import PipelineDF
from sklearndf.transformation import OneHotEncoderDF, ColumnTransformerDF, SimpleImputerDF, StandardScalerDF


# (i) Set up feature transformer pipeline
enc_fac = PipelineDF(steps=[('ohe', OneHotEncoderDF(sparse=False, drop='first'))])
sel_fac = make_column_selector(pattern='^fac\\_')

enc_num = PipelineDF(steps=[('impute', SimpleImputerDF(strategy='median')), ('scale', StandardScalerDF())])
sel_num = make_column_selector(pattern='^num\\_')

enc_df = ColumnTransformerDF(transformers=[('ohe', enc_fac, sel_fac),('s', enc_num, sel_num)])

# (ii) Load datasets
loader = SurvLoader()
ds_lst = loader.df_ds[~loader.df_ds['is_td']]['ds'].to_list()  # Remove datasets with time-varying covariates
n_ds = len(ds_lst)
for i, ds in enumerate(ds_lst):
    print('Dataset %s (%i of %i)' % (ds, i+1, n_ds))
    df, ref = loader.load_dataset(ds).values()
    # Random stratified split
    df_train, df_test = train_test_split(df, stratify=df['event'], random_state=1, test_size=0.3)
    # Fit encoder
    enc_df.fit(df_train)
    # Sanity check
    cn_prefix = enc_df.feature_names_original_.str.split('_',1,True)[0].unique()
    assert all([cn in ['fac', 'num'] for cn in cn_prefix])
    # Prepare numpy arrays

    # Fit model
    mdl = CoxnetSurvivalAnalysis()
    
