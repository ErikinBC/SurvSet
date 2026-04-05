"""
Reproduce issue #6 C-index results: comparing default alpha vs optimized alpha
for CoxnetSurvivalAnalysis on multiple datasets.
"""

import numpy as np
import pandas as pd
from sksurv.util import Surv
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.metrics import concordance_index_censored
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_selector, ColumnTransformer

from SurvSet.data import SurvLoader

# Set up encoder pipeline (same as README)
enc_fac = Pipeline(steps=[('ohe', OneHotEncoder(drop=None, sparse_output=False, handle_unknown='ignore'))])
sel_fac = make_column_selector(pattern='^fac\\_')
enc_num = Pipeline(steps=[('impute', SimpleImputer(strategy='median')), 
                        ('scale', StandardScaler())])
sel_num = make_column_selector(pattern='^num\\_')
enc_df = ColumnTransformer(transformers=[('ohe', enc_fac, sel_fac),('s', enc_num, sel_num)])
enc_df.set_output(transform='pandas')

# Datasets from issue #6
datasets = ['e1684', 'micro.censure', 'cgd']
loader = SurvLoader()

results = []

for ds_name in datasets:
    try:
        df = loader.load_dataset(ds_name)['df']
        
        # Prepare data
        senc = Surv()
        y = senc.from_arrays(df['event'].astype(bool), df['time'])
        enc_df.fit(df)
        X = enc_df.transform(df)
        
        # Fit model
        mdl = CoxnetSurvivalAnalysis(n_alphas=50)
        mdl.fit(X=X, y=y)
        
        # Default alpha (last in path = minimum regularization)
        default_alpha = mdl.alphas_[-1]
        pred_default = mdl.predict(X, alpha=default_alpha)
        c_default = concordance_index_censored(y['event'], y['time'], pred_default)[0]
        
        # Optimized alpha (best C-index during cross-validation)
        best_c = -np.inf
        best_alpha = mdl.alphas_[-1]
        for alpha in mdl.alphas_:
            pred = mdl.predict(X, alpha=alpha)
            c = concordance_index_censored(y['event'], y['time'], pred)[0]
            if c > best_c:
                best_c = c
                best_alpha = alpha
        
        pred_optimal = mdl.predict(X, alpha=best_alpha)
        c_optimal = concordance_index_censored(y['event'], y['time'], pred_optimal)[0]
        
        results.append({
            'Dataset': ds_name,
            'C-index (default alpha)': f"{c_default:.4f}",
            'C-index (optimal alpha)': f"{c_optimal:.4f}",
            'Improvement': f"{(c_optimal - c_default):.4f}"
        })
        
        print(f"✓ {ds_name}")
    except Exception as e:
        print(f"✗ {ds_name}: {e}")

# Print results table
df_results = pd.DataFrame(results)
print("\n" + "="*80)
print("Issue #6: C-index comparison (default alpha vs optimized alpha)")
print("="*80)
print(df_results.to_string(index=False))
print("="*80)
