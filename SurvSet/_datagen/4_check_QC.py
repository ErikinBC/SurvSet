# Ensure all output files follow QC standards
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fold_output', help='Name of the folder where output files will be written (default="output")', default='output')
parser.add_argument('--fold_figures', help='Name of the folder where figures will be stored (default="figures")', default='figures')
parser.add_argument('--min_num', type=int, help='Name of the folder where figures will be stored (default=4)', default='figures')
args = parser.parse_args()
fold_output = args.fold_output
fold_figures = args.fold_figures
min_num = args.min_num
# fold_output='output';fold_figures='figures';min_num=4

import os
import numpy as np
import pandas as pd
import plotnine as pn
from mizani.formatters import custom_format
from funs_ref import di_ref
from funs_support import str_detect, str_subset, makeifnot, find_dir_base

dir_base = find_dir_base()
dir_output = os.path.join(dir_base, fold_output)
dir_figures = os.path.join(dir_base, fold_figures)
makeifnot(dir_figures)
fn_output = pd.Series(os.listdir(dir_output))
is_csv = str_detect(fn_output, 'csv$')
assert is_csv.all(), 'A non-csv file detected in output: %s' % list(fn_output[~is_csv])
n_output = len(fn_output)


################################
# --- (1) LOOP THROUGH ALL --- #

holder = []
for i, fn in enumerate(fn_output):
    ds = fn.replace('.csv','')
    print('--- %s (%i of %i) ---' % (ds, i+1, n_output))
    path_fn = os.path.join(dir_output, fn)
    df = pd.read_csv(path_fn, low_memory=False)
    n = len(df)
    cn_fac = str_subset(df.columns, '^fac\\_')
    cn_num = str_subset(df.columns, '^num\\_')
    n_fac = len(cn_fac)
    n_num = len(cn_num)
    # (i) time is positive
    assert np.all(df['time'] >= 0), 'time is not positive!'
    # (ii) Factors should have no missing
    if n_fac > 0:
        assert df[cn_fac].notnull().any().all(), 'A factor has a missing value!'
        dat_fac = df[cn_fac].apply(lambda x: x.unique().shape[0])
        dat_fac = dat_fac.reset_index().rename(columns={0:'n'}).assign(ds=ds)
        n_ohe = np.sum(dat_fac['n']-1)
    else:
        n_ohe = 0
    # (iii) Numberics have a minimum of Z categories
    if n_num > 0:
        dat_num = df[cn_num].apply(lambda x: x.unique().shape[0])
        dat_num = dat_num.reset_index().rename(columns={0:'n'}).assign(ds=ds)
        assert np.all(dat_num['n'] >= min_num), 'Numeric must have at least %i unique values!' % min_num   
    # (iv) Time dependent checks
    is_td = ('time2' in df.columns)
    if is_td:
        assert np.all(df['time2'] > df['time']), 'time2 is not greater than time!'
        assert df['pid'].duplicated().any(), 'At least one pid must be duplicated!'
    # (v) funs_ref matches each
    assert ds in di_ref, '%s not found in refence!!' % ds
    # (vi) store information
    res = pd.DataFrame({'ds':ds, 'is_td':is_td, 'n':n, 'n_fac':n_fac, 'n_ohe':n_ohe, 'n_num':n_num}, index=[i])
    holder.append(res)
# Merge and save
df_ds = pd.concat(holder)
df_ds.to_csv(os.path.join(dir_figures, 'df_ds.csv'), index=False)


###############################
# --- (2) FIGURES & STATS --- #

# Dimensionality by dataset
df_ds = df_ds.assign(p=lambda x: x['n_ohe']+x['n_num'])
df_ds = df_ds.assign(n_data=lambda x: x['p']*x['n'])
ds_ord = df_ds.sort_values('n_data')['ds'].values
df_ds['ds'] = pd.Categorical(df_ds['ds'], ds_ord)
ds_long = df_ds.melt(['ds','is_td'],['p','n'],'axis','val')

# Plot
format_int = custom_format(fmt='%i', style='old')
gg_ds = (pn.ggplot(ds_long, pn.aes(y='ds',x='val',color='axis',shape='is_td')) + 
    pn.theme_bw() + pn.labs(x='Dataset size') + 
    pn.geom_point() + pn.scale_x_log10(labels=format_int) + 
    pn.theme(axis_title_y=pn.element_blank()) + 
    pn.scale_color_discrete(name='Axis',labels=['Rows','Columns']) + 
    pn.scale_shape_discrete(name='Time-varying'))
gg_ds.save(os.path.join(dir_figures,'gg_ds.png'),height=10, width=6)

print('~~~ End of 4_check_QC.py ~~~')